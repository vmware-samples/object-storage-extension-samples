/**
 * Copyright 2020 program was created by VMware.
 * SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.resource;

import com.vmware.osis.annotation.NotImplement;
import com.vmware.osis.model.OsisCaps;
import org.springframework.beans.factory.InitializingBean;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.json.JsonParseException;
import org.springframework.context.ApplicationContext;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.annotation.RestController;

import java.lang.annotation.Annotation;
import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Predicate;
import java.util.stream.Collectors;

@Component
public class OsisCapsManager implements InitializingBean {

    @Autowired
    private ApplicationContext applicationContext;

    private OsisCaps osisCaps = new OsisCaps();

    @Override
    public void afterPropertiesSet() throws Exception {
        Map<String, Object> rcBeans = getBeans(RestController.class);
        for (Object bean : rcBeans.values()) {
            for (Method method : bean.getClass().getDeclaredMethods()) {
                if (method.isAnnotationPresent(NotImplement.class)) {
                    NotImplement a = method.getAnnotation(NotImplement.class);
                    if (this.osisCaps.getOptionalApis().containsKey(a.name())) {
                        this.osisCaps.getOptionalApis().put(a.name(), false);
                    }
                }
            }
        }
    }

    private Map<String, Object> getBeans(Class<? extends Annotation>... annotationTypes) {
        Map<String, Object> result = new LinkedHashMap<>();
        Arrays.stream(annotationTypes).
                forEach(at -> result.putAll(applicationContext.getBeansWithAnnotation(at)));
        return result;
    }

    private <T> Predicate<T> not(Predicate<T> t) {
        return t.negate();
    }

    public List<String> getNotImplements() {
        return this.osisCaps.getOptionalApis().entrySet().stream().filter(not(Map.Entry::getValue))
                .map(Map.Entry::getKey)
                .collect(Collectors.toList());
    }

    public void updateOsisCaps(OsisCaps caps) {
        if (Boolean.FALSE.equals(caps.isValid())) {
            throw new JsonParseException();
        }
        this.osisCaps.getOptionalApis().forEach((apiCode, status) -> {
            if (caps.getOptionalApis().containsKey(apiCode)) {
                osisCaps.getOptionalApis().put(apiCode, caps.getOptionalApis().get(apiCode));
            }
        });

    }

    public OsisCaps getOsisCaps() {
        return this.osisCaps;
    }
}

