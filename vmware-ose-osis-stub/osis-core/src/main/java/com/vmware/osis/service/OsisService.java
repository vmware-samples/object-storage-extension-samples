/**
 *Copyright 2020 program was created by VMware.
 *SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.service;

import com.vmware.osis.model.*;
import com.vmware.osis.model.OsisCaps;

import java.util.Optional;

public interface OsisService {


    OsisTenant createTenant(OsisTenant osisTenant);

    PageOfTenants queryTenants(long offset, long limit, String filter);

    PageOfTenants listTenants(long offset, long limit);

    OsisTenant getTenant(String tenantId);

    boolean headTenant(String tenantId);

    void deleteTenant(String tenantId, Boolean purgeData);

    OsisTenant updateTenant(String tenantId, OsisTenant osisTenant);

    OsisUser createUser(OsisUser osisUser);

    PageOfUsers queryUsers(long offset, long limit, String filter);

    void deleteUser(String tenantId, String userId, Boolean purgeData);

    OsisUser getUser(String canonicalUserId);

    OsisUser getUser(String tenantId, String userId);

    PageOfUsers listUsers(String tenantId, long offset, long limit);

    OsisUser updateUser(String tenantId, String userId, OsisUser osisUser);

    boolean headUser(String tenantId, String userId);

    OsisS3Credential createS3Credential(String tenantId, String userId);

    PageOfS3Credentials queryS3Credentials(long offset, long limit, String filter);

    void deleteS3Credential(String tenantId, String userId, String accessKey);

    OsisS3Credential getS3Credential(String accessKey);

    PageOfS3Credentials listS3Credentials(String tenantId, String userId, Long offset, Long limit);

    String getProviderConsoleUrl();

    String getTenantConsoleUrl(String tenantId);

    OsisS3Capabilities getS3Capabilities();

    Information getInformation(String domain);

    OsisCaps updateOsisCaps(OsisCaps osisCaps);

    PageOfOsisBucketMeta getBucketList(String tenantId, long offset, long limit);

    OsisUsage getOsisUsage(Optional<String> tenantId, Optional<String> userId);
}
