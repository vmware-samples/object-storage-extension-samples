/**
 *Copyright 2020 program was created by VMware.
 *SPDX-License-Identifier: Apache License 2.0
 */
package com.vmware.osis.security.jwt.model.exception;

import com.fasterxml.jackson.annotation.JsonValue;

public enum ErrorCode {

    AUTHENTICATION(1), JWT_TOKEN_EXPIRED(2);
    
    private int code;

    ErrorCode(int code) {
        this.code = code;
    }

    @JsonValue
    public int getCode() {
        return code;
    }
}
