/**
 *Copyright 2020 program was created by VMware.
 *SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.ceph.utils;

import com.google.common.base.Joiner;
import com.google.common.base.Strings;
import com.vmware.osis.model.Information;
import com.vmware.osis.model.Page;
import com.vmware.osis.model.PageInfo;
import com.vmware.osis.model.exception.BadRequestException;
import org.apache.commons.lang3.StringUtils;
import org.twonote.rgwadmin4j.RgwAdmin;
import org.twonote.rgwadmin4j.impl.RgwAdminException;

import java.net.URI;
import java.util.*;

import static com.vmware.osis.ceph.utils.CephConstants.*;

public final class CephUtil {

    private CephUtil() {
    }


    public static <P extends Page, T> P paginate(long offset, long limit, P page, List<T> items) {
        if (offset < items.size()) {
            long end = (offset + limit) < items.size() ? offset + limit : items.size();
            page.setPageInfo(new PageInfo().total((long) items.size()).offset(offset).limit(limit));
            page.setItems(items.subList((int) offset, (int) end));
            return page;
        } else {
            page.setPageInfo(new PageInfo().total((long) items.size()).offset(offset).limit(limit));
            page.setItems(Collections.emptyList());
            return page;
        }
    }

    public static String extractCdTenantId(String osisTenantId) {
        return osisTenantId.substring(osisTenantId.indexOf(DOUBLE_UNDER_SCORE) + DOUBLE_UNDER_SCORE.length());
    }

    public static String generateCephUid(String tenantId, String userId) {
        return tenantId + DOLLAR + userId;
    }

    public static String normalize(String str) {
        return str == null ? null : str.replace("-", "");
    }


    public static void validateOsisTenantId(String tenantId) {
        if (StringUtils.isNotBlank(tenantId) && !tenantId.contains(DOUBLE_UNDER_SCORE)) {
            throw new BadRequestException(String.format("Invalid OSIS tenant ID %s", tenantId));
        }
    }

    public static Map<String, String> parseFilter(String filter) {
        if (StringUtils.isBlank(filter)) {
            return Collections.emptyMap();
        }

        Map<String, String> kvMap = new HashMap<>();
        Arrays.stream(StringUtils.split(filter, ";"))
                .filter(exp -> exp.contains("==") && exp.indexOf("==") == exp.lastIndexOf("=="))
                .forEach(exp -> {
                    String[] kv = StringUtils.split(exp, "==");
                    if (kv.length == 2) {
                        kvMap.put(kv[0], kv[1]);
                    }

                });
        return kvMap;
    }

    public static String generateFilter(String... kvPairs) {
        if (kvPairs == null || kvPairs.length == 0
                || kvPairs.length % 2 == 1) {
            return null;
        }

        if (kvPairs.length % 2 == 1) {
            return null;
        }

        List<String> exps = new ArrayList<>();
        for (int i = 0; i < kvPairs.length / 2; i++) {
            if (Strings.isNullOrEmpty(kvPairs[2 * i + 1])) {
                continue;
            }
            exps.add(String.format("%s==%s", kvPairs[2 * i], kvPairs[2 * i + 1]));
        }

        return Joiner.on(";").join(exps);
    }

    public static String getLogoPath() {
        return ICON_PATH;
    }

    public static URI getLogoUri(String domain) {
        return URI.create(domain + ICON_PATH);
    }

    public static Information.StatusEnum checkCephStatus(RgwAdmin rgwAdmin) {
        Information.StatusEnum statusEnum = Information.StatusEnum.NORMAL;
        try {
            rgwAdmin.getUsage();
        } catch (RgwAdminException e) {
            statusEnum = Information.StatusEnum.ERROR;
        }
        return statusEnum;
    }


}
