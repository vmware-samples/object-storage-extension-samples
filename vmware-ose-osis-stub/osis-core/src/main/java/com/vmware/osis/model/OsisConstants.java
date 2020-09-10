package com.vmware.osis.model;

import java.util.Arrays;
import java.util.List;

/**
 * Copyright 2020 VMware, Inc.
 * SPDX-License-Identifier: Apache License 2.0
 */
public final class OsisConstants {
    private OsisConstants() {

    }

    public static final String GET_TENANT_API_CODE = "getTenant";
    public static final String DELETE_TENANT_API_CODE = "deleteTenant";
    public static final String HEAD_USER_API_CODE = "headUser";
    public static final String UPDATE_CREDENTIAL_STATUS_API_CODE = "updateCredentialStatus";
    public static final String DELETE_CREDENTIAL_API_CODE = "deleteCredential";
    public static final String GET_USAGE_API_CODE = "getUsage";
    public static final String GET_BUCKET_LIST_API_CODE = "getBucketList";
    public static final String GET_BUCKET_ID_LOGGING_API_CODE = "getBucketLoggingId";
    public static final String GET_ANONYMOUS_USER_API_CODE = "getAnonymousUser";
    public static final String GET_CONSOLE_API_CODE = "getConsole";

    public static final List<String> API_CODES = Arrays.asList(GET_TENANT_API_CODE,
            DELETE_TENANT_API_CODE, HEAD_USER_API_CODE, UPDATE_CREDENTIAL_STATUS_API_CODE,
            DELETE_CREDENTIAL_API_CODE, GET_USAGE_API_CODE, GET_BUCKET_LIST_API_CODE,
            GET_BUCKET_ID_LOGGING_API_CODE, GET_ANONYMOUS_USER_API_CODE, GET_CONSOLE_API_CODE);
}
