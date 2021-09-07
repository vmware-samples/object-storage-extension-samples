/**
 *Copyright 2020 VMware, Inc.
 *SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.ceph.utils;

public final class CephConstants {

    private CephConstants() {
    }


    //display name
    //attr1::value1;value2;;attr2::value3
    public static final String DOLLAR = "$";
    public static final String COMMA = ",";
    public static final String DOUBLE_UNDER_SCORE = "__";

    public static final String ARRAY_SEPARATOR = ";";
    public static final String ATTRIBUTE_SEPARATOR = ";;";
    public static final String ATTRIBUTE_EQUAL_SIGN = "::";

    public static final String ATTRIBUTE_CD_TENANT_IDS = "cdtids";
    public static final String ATTRIBUTE_CD_TENANT_ID = "cdtid";
    public static final String ATTRIBUTE_CD_USER_ID = "cduid";
    public static final String ATTRIBUTE_USERNAME = "un";

    public static final String OSIS_TENANT_ID = "tenant_id";
    public static final String OSIS_CD_TENANT_ID = "cd_tenant_id";
    public static final String OSIS_USER_ID = "user_id";
    public static final String OSIS_CD_USER_ID = "cd_user_id";
    public static final String OSIS_CANONICAL_USER_ID = "canonical_user_id";
    public static final String OSIS_DISPLAY_NAME = "display_name";
    public static final String OSIS_ACCESS_KEY = "access_key";
    public static final String OSIS_ACTIVE = "active";
    public static final String ICON_PATH = "/ceph.png";
    public static final String IAM_PREFIX = "/admin";
}
