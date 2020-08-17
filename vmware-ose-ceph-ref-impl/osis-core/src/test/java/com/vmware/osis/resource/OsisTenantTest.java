/**
 *Copyright 2020 program was created by VMware.
 *SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.resource;

import com.vmware.osis.model.OsisTenant;
import org.junit.jupiter.api.*;
import org.mockito.Mock;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MvcResult;
import org.twonote.rgwadmin4j.RgwAdmin;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

public class OsisTenantTest extends OsisControllerTestBase {

    @Mock
    private RgwAdmin rgwAdmin;

    @Test
    public void testCreateTenantExceptOK() throws Exception {
        clear();
        MvcResult result = mockMvc.perform(post(CREATE_TENANT_PATH)
                .contentType(MediaType.APPLICATION_JSON)
                .content(mapper.writeValueAsBytes(mockCreateOsisTenant())))
                .andExpect(status().isOk())
                .andReturn();
        String response = result.getResponse().getContentAsString();
        OsisTenant tenant = mapper.readValue(response, OsisTenant.class);
        Assertions.assertEquals(tenant, exceptOsisTenant());
        clear();
    }

    @Test
    public void testGetTenant() throws Exception {
        clear();
        prepare();
        String response = mockMvc.perform(get(GET_TENANT_PATH1))
                .andExpect(status().isOk())
                .andReturn().getResponse().getContentAsString();
        OsisTenant tenant = mapper.readValue(response, OsisTenant.class);
        Assertions.assertEquals(tenant, exceptOsisTenant1());
        clear();
    }

    @Test
    public void testCheckTenant() throws Exception {
        clear();
        prepare();
        mockMvc.perform(head(CHECK_TENANT_PATH1))
                .andExpect(status().isOk());
        clear();
    }

    @Test
    public void testListTenant() throws Exception {
        clear();
        prepare();
        String got = mockMvc.perform(get(LIST_TENANT_PATH).param(OFFSET, OFFSET_VALUE).param(LIMIT, LIMIT_VALUE))
                .andExpect(status().isOk())
                .andReturn().getResponse().getContentAsString();
        String want = mapper.writeValueAsString(exceptOsisTenant());
        Assertions.assertEquals(got, want);
        clear();
    }

    @Test
    public void testQueryTenant() throws Exception {
        clear();
        prepare();
        String got = mockMvc.perform(get(QUERY_TENANT_PATH)
                .param(FILTER, FILTER_BY_CD_TENANT1))
                .andExpect(status().isOk())
                .andDo(print())
                .andReturn().getResponse().getContentAsString();
        String want = mapper.writeValueAsString(exceptPageOfTenants1());
        Assertions.assertEquals(got, want);
        clear();
    }

    public void prepare() throws Exception{
        mockMvc.perform(post(CREATE_TENANT_PATH)
                .contentType(MediaType.APPLICATION_JSON)
                .content(mapper.writeValueAsBytes(mockCreateOsisTenant1()))).andExpect(status().isOk());

        mockMvc.perform(post(CREATE_TENANT_PATH)
                .contentType(MediaType.APPLICATION_JSON)
                .content(mapper.writeValueAsBytes(mockCreateOsisTenant2())))
                .andExpect(status().isOk());
    }

    public void clear() throws Exception {
        mockMvc.perform(delete(CLEAR_TENANT_PATH).queryParam(PURGE_DATA, "true"))
                .andExpect(status().is2xxSuccessful());
        mockMvc.perform(delete(CLEAR_TENANT_PATH1).queryParam(PURGE_DATA, "true"))
                .andExpect(status().is2xxSuccessful());
        mockMvc.perform(delete(CLEAR_TENANT_PATH2).queryParam(PURGE_DATA, "true"))
                .andExpect(status().is2xxSuccessful());
    }

}
