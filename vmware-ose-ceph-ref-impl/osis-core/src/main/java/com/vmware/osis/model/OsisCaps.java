/**
 *Copyright 2020 program was created by VMware.
 *SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.HashMap;
import java.util.Map;

public class OsisCaps {
    @JsonProperty
    private final Map<String, Boolean> optionalApis = new HashMap<>();

    public OsisCaps() {
        OsisConstants.API_CODES.forEach(name -> optionalApis.put(name, true));
    }

    public Map<String, Boolean> getOptionalApis() {
        return optionalApis;
    }

    @JsonIgnore
    public Boolean isValid() {
        return OsisConstants.API_CODES.containsAll(optionalApis.keySet());
    }
}
