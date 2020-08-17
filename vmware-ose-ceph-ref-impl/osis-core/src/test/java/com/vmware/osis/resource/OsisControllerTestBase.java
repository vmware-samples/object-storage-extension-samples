/**
 *Copyright 2020 program was created by VMware.
 *SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.resource;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.vmware.osis.model.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

import java.util.Arrays;

@SpringBootTest
@AutoConfigureMockMvc
public class OsisControllerTestBase {

    protected static final String TENANT_NAME = "tenant";
    protected static final String TENANT_NAME1 = "tenant1";
    protected static final String TENANT_NAME2 = "tenant2";
    protected static final String CD_TENANT_ID1 = "cdTenantId1";
    protected static final String CD_TENANT_ID2 = "cdTenantId2";
    protected static final String CD_TENANT_ID3 = "cdTenantId3";
    protected static final Boolean TENANT_ACTIVE = true;
    protected static final String PURGE_DATA = "purge_data";
    protected static final String TENANT_PATH = "/api/v1/tenants";
    protected static final String SLASH = "/";
    protected static final String CREATE_TENANT_PATH = TENANT_PATH;
    protected static final String GET_TENANT_PATH = TENANT_PATH + SLASH + TENANT_NAME;
    protected static final String CLEAR_TENANT_PATH = TENANT_PATH + SLASH + TENANT_NAME;
    protected static final String CLEAR_TENANT_PATH1 = TENANT_PATH + SLASH + TENANT_NAME1;
    protected static final String CLEAR_TENANT_PATH2 = TENANT_PATH + SLASH + TENANT_NAME2;
    protected static final String GET_TENANT_PATH1 = TENANT_PATH + SLASH + TENANT_NAME1;
    protected static final String CHECK_TENANT_PATH1= GET_TENANT_PATH1;
    protected static final String LIST_TENANT_PATH = TENANT_PATH;
    protected static final String QUERY_TENANT_PATH = TENANT_PATH + SLASH + "query";
    protected static final String OFFSET = "offset";
    protected static final String OFFSET_VALUE = "0";
    protected static final String LIMIT = "limit";
    protected static final String LIMIT_VALUE = "10";
    protected static final String FILTER = "filter";
    protected static final String FILTER_BY_CD_TENANT1 = "cd_tenant_id=" + CD_TENANT_ID1;

    protected static final String CREATE_USER_PATH = "api/v1/tenants/tenant1/users";
    protected static final String LIST_USER_PATH = CREATE_USER_PATH;
    protected static final String GET_USER_PATH = "api/vi/tenants/tenant1/users/user1";
    protected static final String GET_USER_CANONICAL_PATH = "api/v1/users/tenant1$user1";
    protected static final String UPDATE_USER_PATH = GET_USER_PATH;

    protected static final String CREATE_S3_PATH = "api/v1/tenants/tenant1/users/user1/s3credentials";
    protected static final String LIST_S3_PATH = CREATE_S3_PATH;


    @Autowired
    protected MockMvc mockMvc;

    @Autowired
    protected ObjectMapper mapper;

    protected OsisTenant mockCreateOsisTenant() {
        return new OsisTenant()
                .name(TENANT_NAME)
                .active(TENANT_ACTIVE)
                .cdTenantIds(Arrays.asList(CD_TENANT_ID1,CD_TENANT_ID2));
    }

    protected OsisTenant mockCreateOsisTenant1() {
        return mockCreateOsisTenant().name(TENANT_NAME1)
                .cdTenantIds(Arrays.asList(CD_TENANT_ID1,CD_TENANT_ID2));
    }

    protected OsisTenant mockCreateOsisTenant2() {
        return mockCreateOsisTenant().name(TENANT_NAME2)
                .cdTenantIds(Arrays.asList(CD_TENANT_ID2, CD_TENANT_ID3));
    }

    protected OsisTenant exceptOsisTenant() {
        return mockCreateOsisTenant().tenantId(TENANT_NAME);
    }

    protected OsisTenant exceptOsisTenant1() { return mockCreateOsisTenant1().tenantId(TENANT_NAME1);}

    protected OsisTenant exceptOsisTenant2() { return mockCreateOsisTenant2().tenantId(TENANT_NAME2);}

    protected PageOfTenants exceptPageOfTenants() {
        return new PageOfTenants()
                .addItemsItem(exceptOsisTenant1())
                .addItemsItem(exceptOsisTenant2())
                .pageInfo(new PageInfo().total(2L).offset(0L).limit(10L));
    }

    protected PageOfTenants exceptPageOfTenants1() {
        return new PageOfTenants()
                .addItemsItem(mockCreateOsisTenant1().tenantId(TENANT_NAME1))
                .pageInfo(new PageInfo().total(1L).offset(0L).limit(10L));
    }

    protected OsisUser mockCreateOsisUser() {
        return new OsisUser()
                .tenantId("tenant1")
                .cdUserId("user1")
                .cdTenantId("cdTenant1")
                .active(true)
                .displayName("rachelw")
                .email("user1@vmware.com")
                .role(OsisUser.RoleEnum.TENANT_ADMIN);
    }

    protected OsisUser exceptOsisUser() {
        return mockCreateOsisUser().userId("user1").canonicalUserId("tenant1$user1");
    }

    protected PageOfUsers exceptListOsisUser() {
        return new PageOfUsers()
                .addItemsItem(exceptOsisUser())
                .pageInfo(new PageInfo().total(1L).offset(0L).limit(10L));
    }

    protected OsisUser mockUpdateOsisUser() {
        return new OsisUser().active(false);
    }

    protected OsisUser exceptUpdateOsisUser() {
        return exceptOsisUser().active(false);
    }
}
