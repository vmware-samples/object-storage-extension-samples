/**
 *Copyright 2020 program was created by VMware.
 *SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.resource;

import com.vmware.osis.model.OsisUser;
import com.vmware.osis.model.PageOfUsers;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.springframework.http.MediaType;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultHandlers.print;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

public class OsisUserTest extends OsisControllerTestBase{

    @Test
    public void perpare() throws Exception {
        mockMvc.perform(post(CREATE_TENANT_PATH)
                .contentType(MediaType.APPLICATION_JSON)
                .content(mapper.writeValueAsBytes(mockCreateOsisTenant1())))
                .andExpect(status().isOk())
                .andDo(print());
    }

    @Test
    public void testCreateUser () throws Exception{
        String response = mockMvc.perform(post(CREATE_USER_PATH)
                .contentType(MediaType.APPLICATION_JSON)
                .content(mapper.writeValueAsBytes(mockCreateOsisUser())))
                .andExpect(status().isOk())
                .andReturn().getResponse().getContentAsString();
        OsisUser user = mapper.readValue(response, OsisUser.class);
        Assertions.assertEquals(user, exceptOsisUser());
    }

    @Test
    public void testListUser() throws Exception{
        String response = mockMvc.perform(get(LIST_USER_PATH)
                .param(OFFSET, OFFSET_VALUE).param(LIMIT, LIMIT_VALUE))
                .andExpect(status().isOk())
                .andReturn().getResponse().getContentAsString();
        PageOfUsers users = mapper.readValue(response, PageOfUsers.class);
        Assertions.assertEquals(users, exceptListOsisUser());
    }

    @Test
    public void testGetUserWithUserId() throws Exception{
        String response = mockMvc.perform(get(GET_USER_PATH))
                .andExpect(status().isOk())
                .andReturn().getResponse().getContentAsString();
        OsisUser user = mapper.readValue(response, OsisUser.class);
        Assertions.assertEquals(user, exceptOsisUser());
    }

    @Test
    public void testGetUserWithCanonicalUserId() throws Exception{
        String response = mockMvc.perform(get(GET_USER_CANONICAL_PATH))
                .andExpect(status().isOk())
                .andReturn().getResponse().getContentAsString();
        OsisUser user = mapper.readValue(response, OsisUser.class);
        Assertions.assertEquals(user, exceptOsisUser());
    }

    @Test
    public void testUpdateUserStatus() throws Exception{
        String response = mockMvc.perform(patch(UPDATE_USER_PATH)
        .contentType(MediaType.APPLICATION_JSON)
        .content(mapper.writeValueAsBytes(mockUpdateOsisUser())))
                .andExpect(status().isOk())
                .andReturn().getResponse().getContentAsString();
        OsisUser user = mapper.readValue(response, OsisUser.class);
        Assertions.assertEquals(user, exceptUpdateOsisUser());
    }
}
