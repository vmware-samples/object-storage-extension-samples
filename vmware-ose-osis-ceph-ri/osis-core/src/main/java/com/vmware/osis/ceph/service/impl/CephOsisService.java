/**
 * Copyright 2020 VMware, Inc.
 * SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.ceph.service.impl;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.vmware.osis.ceph.AppEnv;
import com.vmware.osis.ceph.utils.CephUtil;
import com.vmware.osis.ceph.utils.ModelConverter;
import com.vmware.osis.model.*;
import com.vmware.osis.model.exception.BadRequestException;
import com.vmware.osis.model.exception.InternalException;
import com.vmware.osis.model.exception.NotFoundException;
import com.vmware.osis.resource.OsisCapsManager;
import com.vmware.osis.service.OsisService;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;
import org.twonote.rgwadmin4j.RgwAdmin;
import org.twonote.rgwadmin4j.model.BucketInfo;
import org.twonote.rgwadmin4j.model.S3Credential;
import org.twonote.rgwadmin4j.model.User;

import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;

import static com.vmware.osis.ceph.utils.CephUtil.*;
import static com.vmware.osis.ceph.utils.ModelConverter.*;
import static com.vmware.osis.ceph.utils.CephConstants.*;


@Service
public class CephOsisService implements OsisService {
    private static final Logger logger = LoggerFactory.getLogger(CephOsisService.class);
    private static final String S3_CAPABILITIES_JSON = "s3capabilities.json";

    @Autowired
    private AppEnv appEnv;

    @Autowired
    private RgwAdmin rgwAdmin;

    @Autowired
    private OsisCapsManager osisCapsManager;

    private static final String CEPH_PARAM_TENANT = "tenant";
    private static final String CEPH_PARAM_SUSPENDED = "suspended";
    private static final String CEPH_PARAM_DISPLAY_NAME = "display-name";
    private static final String CEPH_PARAM_USER_CAPS = "user-caps";
    private static final String CEPH_PARAM_EMAIL = "email";

    @Override
    public OsisTenant createTenant(OsisTenant osisTenant) {
        User user = ModelConverter.toCephUser(osisTenant);

        Map<String, String> parameters = new HashMap<>();
        parameters.put(CEPH_PARAM_TENANT, user.getTenant());
        parameters.put(CEPH_PARAM_SUSPENDED, Boolean.toString(user.getSuspended() == 1));
        parameters.put(CEPH_PARAM_DISPLAY_NAME, user.getDisplayName());

        return ModelConverter.toOsisTenant(rgwAdmin.createUser(user.getUserId(), parameters));
    }

    @Override
    public PageOfTenants queryTenants(long offset, long limit, String filter) {
        Map<String, String> kvMap = parseFilter(filter);
        String tenantId = kvMap.get(OSIS_TENANT_ID);
        String cdTenantId = kvMap.get(OSIS_CD_TENANT_ID);

        List<String> tenantUids = rgwAdmin.listUser().stream()
                .filter(uid -> uid.contains(DOLLAR) && uid.indexOf(DOLLAR) == uid.length() / 2).collect(Collectors.toList());

        if (StringUtils.isNotBlank(tenantId)) {
            tenantUids = tenantUids.stream().filter(uid -> uid.equals(generateCephUid(toCephTenantId(tenantId), toCephTenantId(tenantId)))).collect(Collectors.toList());
        }

        if (tenantUids.isEmpty()) {
            return paginate(offset, limit, new PageOfTenants(), Collections.emptyList());
        }

        List<OsisTenant> tenants = tenantUids.stream().map(tenantUid -> rgwAdmin.getUserInfo(tenantUid))
                .filter(Optional::isPresent).map(u -> ModelConverter.toOsisTenant(u.get())).collect(Collectors.toList());

        if (StringUtils.isBlank(cdTenantId)) {
            return paginate(offset, limit, new PageOfTenants(), tenants);

        }

        return paginate(offset, limit, new PageOfTenants(), tenants.stream().filter(t -> t.getCdTenantIds().contains(cdTenantId)).collect(Collectors.toList()));

    }

    @Override
    public PageOfTenants listTenants(long offset, long limit) {
        return this.queryTenants(offset, limit, null);
    }

    @Override
    public OsisUser createUser(OsisUser osisUser) {

        if (!headTenant(osisUser.getTenantId())) {
            throw new BadRequestException(String.format("The tenant %s does not exist.", osisUser.getTenantId()));
        }

        if (hasUser(osisUser.getTenantId(), osisUser.getUserId())) {
            return getUser(osisUser.getTenantId(), osisUser.getUserId());
        }

        User user = ModelConverter.toCephUser(osisUser);

        Map<String, String> parameters = new HashMap<>();
        parameters.put(CEPH_PARAM_TENANT, user.getTenant());
        parameters.put(CEPH_PARAM_DISPLAY_NAME, user.getDisplayName());
        parameters.put(CEPH_PARAM_SUSPENDED, Boolean.toString(user.getSuspended() == 1));
        parameters.put(CEPH_PARAM_USER_CAPS, toCephCapsParam(user.getCaps()));
        parameters.put(CEPH_PARAM_EMAIL, osisUser.getEmail());
        return ModelConverter.toOsisUser(rgwAdmin.createUser(user.getUserId(), parameters));

    }

    @Override
    public PageOfUsers queryUsers(long offset, long limit, String filter) {
        Map<String, String> kvMap = parseFilter(filter);
        String tenantId = kvMap.get(OSIS_TENANT_ID);
        String cdTenantId = kvMap.get(OSIS_CD_TENANT_ID);
        String userId = kvMap.get(OSIS_USER_ID);
        String cdUserId = kvMap.get(OSIS_CD_USER_ID);
        String canonicalUserId = kvMap.get(OSIS_CANONICAL_USER_ID);
        String displayName = kvMap.get(OSIS_DISPLAY_NAME);
        String activeStr = kvMap.get(OSIS_ACTIVE);


        List<String> uids = rgwAdmin.listUser().stream()
                .filter(uid -> uid.contains(DOLLAR)).collect(Collectors.toList());
        uids = filterCephUids(uids, canonicalUserId, tenantId, userId);

        if (uids.isEmpty()) {
            return paginate(offset, limit, new PageOfUsers(), Collections.emptyList());
        }

        List<OsisUser> osisUsers = uids.stream().map(tenantUid -> rgwAdmin.getUserInfo(tenantUid))
                .filter(Optional::isPresent).map(u -> ModelConverter.toOsisUser(u.get())).collect(Collectors.toList());
        osisUsers = filterOsisUsers(osisUsers, displayName, cdTenantId, cdUserId, activeStr, null);

        return paginate(offset, limit, new PageOfUsers(), osisUsers);
    }

    private List<String> filterCephUids(List<String> uids, String canonicalUserId, String tenantId, String userId) {
        uids = uids.stream().filter(uid ->
                (StringUtils.isBlank(canonicalUserId) || uid.equals(canonicalUserId))
                        && (StringUtils.isBlank(tenantId) || uid.startsWith(toCephTenantId(tenantId) + DOLLAR))
                        && (StringUtils.isBlank(userId) || uid.endsWith(DOLLAR + userId))
        ).collect(Collectors.toList());
        return uids;
    }


    @Override
    public OsisS3Credential createS3Credential(String tenantId, String userId) {
        Optional<User> cephUser = rgwAdmin.getUserInfo(generateCephUid(toCephTenantId(tenantId), userId));
        if (!cephUser.isPresent()) {
            throw new BadRequestException(String.format("The specific user %s in tenant %s doesn't exist", userId, tenantId));
        }

        List<S3Credential> existingS3Credentials = cephUser.get().getS3Credentials();
        Set<S3Credential> newS3Credentials = new HashSet<>(rgwAdmin.createS3Credential(generateCephUid(toCephTenantId(tenantId), userId)));
        newS3Credentials.removeAll(existingS3Credentials);

        if (newS3Credentials.size() == 1) {
            return toOsisS3Credential(cephUser.get(), newS3Credentials.iterator().next());
        }
        throw new InternalException(String.format("Fail to create credential for user %s in tenant %s", userId, tenantId));
    }

    @Override
    public PageOfS3Credentials queryS3Credentials(long offset, long limit, String filter) {
        Map<String, String> kvMap = parseFilter(filter);
        String tenantId = kvMap.get(OSIS_TENANT_ID);
        String cdTenantId = kvMap.get(OSIS_CD_TENANT_ID);
        String userId = kvMap.get(OSIS_USER_ID);
        String cdUserId = kvMap.get(OSIS_CD_USER_ID);
        String activeStr = kvMap.get(OSIS_ACTIVE);
        String accessKey = kvMap.get(OSIS_ACCESS_KEY);


        List<String> uids = rgwAdmin.listUser().stream()
                .filter(uid -> uid.contains(DOLLAR)).collect(Collectors.toList());
        uids = filterCephUids(uids, null, tenantId, userId);
        if (uids.isEmpty()) {
            return paginate(offset, limit, new PageOfS3Credentials(), Collections.emptyList());
        }

        List<OsisUser> osisUsers = uids.stream().map(tenantUid -> rgwAdmin.getUserInfo(tenantUid))
                .filter(Optional::isPresent)
                .map(u -> ModelConverter.toOsisUser(u.get())).collect(Collectors.toList());
        osisUsers = filterOsisUsers(osisUsers, null, cdTenantId, cdUserId, activeStr, accessKey);

        List<OsisS3Credential> s3Credentials = osisUsers.stream().flatMap(osisUser ->
                osisUser.getOsisS3Credentials().stream().filter(c -> StringUtils.isBlank(accessKey) || c.getAccessKey().equals(accessKey))).collect(Collectors.toList());
        return paginate(offset, limit, new PageOfS3Credentials(), s3Credentials);
    }

    private List<OsisUser> filterOsisUsers(List<OsisUser> osisUsers, String displayName, String cdTenantId, String cdUserId, String activeStr, String accessKey) {
        osisUsers = osisUsers.stream().filter(osisUser ->
                        (StringUtils.isBlank(accessKey) || osisUser.getOsisS3Credentials().stream().anyMatch(c -> c.getAccessKey().equals(accessKey)))
                                && (StringUtils.isBlank(displayName) || displayName.equals(osisUser.getUsername()))
                                && (StringUtils.isBlank(activeStr) || osisUser.getActive() == Boolean.parseBoolean(activeStr))
                                && (StringUtils.isBlank(cdTenantId) || cdTenantId.equals(osisUser.getCdTenantId()))
                                && (StringUtils.isBlank(cdUserId) || cdUserId.equals(osisUser.getCdUserId())))
                .collect(Collectors.toList());
        return osisUsers;
    }


    @Override
    public String getProviderConsoleUrl() {
        return appEnv.getConsoleEndpoint();
    }

    @Override
    public String getTenantConsoleUrl(String tenantId) {
        return appEnv.getConsoleEndpoint();
    }

    @Override
    public OsisS3Capabilities getS3Capabilities() {
        OsisS3Capabilities osisS3Capabilities = new OsisS3Capabilities();
        try {
            osisS3Capabilities = new ObjectMapper()
                    .readValue(new ClassPathResource(S3_CAPABILITIES_JSON).getInputStream(),
                            OsisS3Capabilities.class);
        } catch (IOException e) {
            logger.info("Fail to load S3 capabilities from configuration file {}.", S3_CAPABILITIES_JSON);
        }
        return osisS3Capabilities;
    }

    @Override
    public void deleteS3Credential(String tenantId, String userId, String accessKey) {
        PageOfS3Credentials pageOfS3Credentials = this.queryS3Credentials(0L, 1L, CephUtil.generateFilter(OSIS_TENANT_ID, tenantId, OSIS_USER_ID, userId, OSIS_ACCESS_KEY, accessKey));
        if (pageOfS3Credentials.getPageInfo().getTotal() > 0) {
            rgwAdmin.removeS3Credential(generateCephUid(toCephTenantId(pageOfS3Credentials.getItems().get(0).getTenantId()), pageOfS3Credentials.getItems().get(0).getUserId()), accessKey);
        }
    }

    @Override
    public void deleteTenant(String tenantId, Boolean purgeData) {
        rgwAdmin.removeUser(generateCephUid(toCephTenantId(tenantId), tenantId), purgeData);
    }

    @Override
    public OsisTenant updateTenant(String tenantId, OsisTenant osisTenant) {
        this.headTenant(tenantId);

        User user = ModelConverter.toCephUser(osisTenant);

        Map<String, String> parameters = new HashMap<>();
        if (StringUtils.isNotBlank(user.getTenant())) {
            parameters.put(CEPH_PARAM_TENANT, user.getTenant());
        }
        if (user.getSuspended() != null) {
            parameters.put(CEPH_PARAM_SUSPENDED, Boolean.toString(user.getSuspended() == 1));
        }
        if (StringUtils.isNotBlank(user.getDisplayName())) {
            parameters.put(CEPH_PARAM_DISPLAY_NAME, user.getDisplayName());
        }


        return ModelConverter.toOsisTenant(rgwAdmin.modifyUser(generateCephUid(toCephTenantId(tenantId), tenantId), parameters));
    }

    @Override
    public void deleteUser(String tenantId, String userId, Boolean purgeData) {
        try {
            if (!hasUser(tenantId, userId)) {
                return;
            }
        } catch (Exception e) {
            return;
        }
        rgwAdmin.removeUser(generateCephUid(toCephTenantId(tenantId), userId), purgeData);
    }

    @Override
    public OsisS3Credential getS3Credential(String accessKey) {
        PageOfS3Credentials pageOfS3Credentials = this.queryS3Credentials(0L, 1L, CephUtil.generateFilter(OSIS_ACCESS_KEY, accessKey));

        if (pageOfS3Credentials.getPageInfo().getTotal() < 1) {
            throw new NotFoundException("S3 credential not found");
        }

        return pageOfS3Credentials.getItems().get(0);
    }

    @Override
    public OsisTenant getTenant(String tenantId) {
        Optional<User> tenant = this.rgwAdmin.getUserInfo(generateCephUid(toCephTenantId(tenantId), toCephTenantId(tenantId)));
        if (!tenant.isPresent()) {
            throw new NotFoundException("The tenant not found");
        }

        return ModelConverter.toOsisTenant(tenant.get());
    }

    @Override
    public OsisUser getUser(String canonicalUserId) {
        Optional<User> user = this.rgwAdmin.getUserInfo(canonicalUserId);
        if (!user.isPresent()) {
            throw new NotFoundException("The user not found");
        }

        return ModelConverter.toOsisUser(user.get());
    }

    @Override
    public OsisUser getUser(String tenantId, String userId) {

        Optional<User> user = this.rgwAdmin.getUserInfo(generateCephUid(toCephTenantId(tenantId), userId));
        if (!user.isPresent()) {
            throw new NotFoundException("The user not found");
        }

        return ModelConverter.toOsisUser(user.get());

    }

    @Override
    public boolean headTenant(String tenantId) {
        try {
            return this.getTenant(tenantId) != null;
        } catch (Exception e) {
            throw new NotFoundException(String.format("No tenant found with tenantId=%s", tenantId));
        }
    }

    @Override
    public boolean headUser(String tenantId, String userId) {
        if (hasUser(tenantId, userId)) {
            return true;
        } else {
            throw new NotFoundException(String.format("No user found with tenantId=%s and userId=%s", tenantId, userId));
        }
    }

    @Override
    public PageOfS3Credentials listS3Credentials(String tenantId, String userId, Long offset, Long limit) {
        return this.queryS3Credentials(offset, limit, CephUtil.generateFilter(OSIS_TENANT_ID, tenantId, OSIS_USER_ID, userId));
    }

    @Override
    public PageOfUsers listUsers(String tenantId, long offset, long limit) {
        return this.queryUsers(offset, limit, CephUtil.generateFilter(OSIS_TENANT_ID, tenantId));
    }

    @Override
    public OsisUser updateUser(String tenantId, String userId, OsisUser osisUser) {
        Map<String, String> parameters = new HashMap<>();
        parameters.put(CEPH_PARAM_SUSPENDED, String.valueOf(!osisUser.getActive()));
        return ModelConverter.toOsisUser(rgwAdmin.modifyUser(generateCephUid(toCephTenantId(tenantId), userId), parameters));
    }

    @Override
    public Information getInformation(String domain) {
        return new Information()
                .addAuthModesItem(appEnv.isApiTokenEnabled() ? Information.AuthModesEnum.BEARER : Information.AuthModesEnum.BASIC)
                .storageClasses(appEnv.getStorageInfo())
                .regions(appEnv.getRegionInfo())
                .platformName(appEnv.getPlatformName())
                .platformVersion(appEnv.getPlatformVersion())
                .apiVersion(appEnv.getApiVersion())
                .notImplemented(osisCapsManager.getNotImplements())
                .logoUri(CephUtil.getLogoUri(domain))
                .services(new InformationServices().iam(domain + IAM_PREFIX).s3(appEnv.getS3Endpoint()))
                .status(CephUtil.checkCephStatus(rgwAdmin));
    }

    @Override
    public OsisCaps updateOsisCaps(OsisCaps osisCaps) {
        osisCapsManager.updateOsisCaps(osisCaps);
        return osisCapsManager.getOsisCaps();
    }

    @Override
    public PageOfOsisBucketMeta getBucketList(String tenantId, long offset, long limit) {
        List<OsisBucketMeta> buckets = new ArrayList<>();
        rgwAdmin.listUser().stream()
                .filter(uid -> uid.startsWith(toCephTenantId(tenantId) + DOLLAR))
                .forEach(uid -> buckets.addAll(rgwAdmin.listBucketInfo(uid).stream().map(ModelConverter::toOsisBucketMeta)
                        .collect(Collectors.toList())));

        return paginate(offset, limit, new PageOfOsisBucketMeta(), buckets);
    }

    @Override
    public OsisUsage getOsisUsage(Optional<String> tenantId, Optional<String> userId) {
        List<BucketInfo> bi;
        if (tenantId.isPresent() && userId.isPresent()) {
            bi = rgwAdmin.listBucketInfo(generateCephUid(toCephTenantId(tenantId.get()), userId.get()));
        } else if (tenantId.isPresent()) {

            List<String> uidsBelongToTenant = rgwAdmin.listUser().stream()
                    .filter(uid -> uid.startsWith(toCephTenantId(tenantId.get()) + DOLLAR)).collect(Collectors.toList());
            return uidsBelongToTenant.stream().map(uid -> ModelConverter.toOsisUsage(rgwAdmin.listBucketInfo(uid)))
                    .reduce(new OsisUsage(), (u1, u2) -> {
                        OsisUsage usage = new OsisUsage();
                        usage.setTotalBytes(u1.getTotalBytes() + u2.getTotalBytes());
                        usage.setAvailableBytes(u1.getAvailableBytes() + u2.getAvailableBytes());
                        usage.setUsedBytes(u1.getUsedBytes() + u2.getUsedBytes());
                        usage.setBucketCount(u1.getBucketCount() + u2.getBucketCount());
                        usage.setObjectCount(u1.getObjectCount() + u2.getObjectCount());
                        return usage;
                    });
        } else {
            bi = rgwAdmin.listBucketInfo();
        }
        return ModelConverter.toOsisUsage(bi);
    }

    private boolean hasUser(String tenantId, String userId) {
        try {
            return this.getUser(tenantId, userId) != null;
        } catch (Exception e) {
            logger.info("No user found with tenantId={} and userId={}", tenantId, userId);
            return false;
        }
    }
}
