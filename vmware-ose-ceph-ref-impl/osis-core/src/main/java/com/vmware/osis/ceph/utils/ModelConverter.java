/**
 * Copyright 2020 VMware, Inc.
 * SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.ceph.utils;

import com.vmware.osis.model.*;
import org.apache.commons.lang3.StringUtils;
import org.twonote.rgwadmin4j.model.BucketInfo;
import org.twonote.rgwadmin4j.model.Cap;
import org.twonote.rgwadmin4j.model.S3Credential;
import org.twonote.rgwadmin4j.model.User;

import java.util.*;
import java.util.stream.Collectors;

import static com.vmware.osis.ceph.utils.CephConstants.*;
import static com.vmware.osis.model.OsisUser.RoleEnum;

public final class ModelConverter {


    private ModelConverter() {
    }

    public static User toCephUser(OsisTenant osisTenant) {
        User user = new User();
        if (StringUtils.isBlank(osisTenant.getTenantId())) {
            user.setTenant(toCephTenantId(osisTenant.getName(), osisTenant.getCdTenantIds().get(0)));
            user.setUserId(toCephTenantId(osisTenant.getName(), osisTenant.getCdTenantIds().get(0)));
        } else {
            user.setTenant(osisTenant.getTenantId());
            user.setUserId(osisTenant.getTenantId());
        }

        user.setSuspended(osisTenant.getActive() ? 0 : 1);
        user.setDisplayName(
                new DisplayNameRecordGenerator()
                        .appendAttribute(ATTRIBUTE_CD_TENANT_IDS, osisTenant.getCdTenantIds()).generate());
        return user;
    }

    public static User toCephUser(OsisUser osisUser) {
        User user = new User();
        user.setTenant(osisUser.getTenantId());
        user.setUserId(osisUser.getCdUserId());
        user.setEmail(osisUser.getEmail());
        user.setCaps(toCephCaps(osisUser.getRole()));

        if (osisUser.getActive() != null) {
            user.setSuspended(osisUser.getActive().booleanValue() ? 0 : 1);
        }

        user.setDisplayName(
                new DisplayNameRecordGenerator()
                        .appendAttribute(ATTRIBUTE_USERNAME, osisUser.getUsername())
                        .appendAttribute(ATTRIBUTE_CD_TENANT_ID, osisUser.getCdTenantId())
                        .appendAttribute(ATTRIBUTE_CD_USER_ID, osisUser.getCdUserId())
                        .generate());

        return user;
    }

    public static OsisS3Credential toOsisS3Credential(User user, S3Credential s3Credential) {
        DisplayNameRecordParser parser = new DisplayNameRecordParser(user.getDisplayName());
        return new OsisS3Credential().accessKey(s3Credential.getAccessKey())
                .secretKey(s3Credential.getSecretKey())
                .active(null)
                .immutable(false)
                .tenantId(toOsisTenantId(user.getTenant()))
                .userId(user.getUserId())
                .username(parser.getAttributeValue(ATTRIBUTE_USERNAME))
                .cdTenantId(parser.getAttributeValue(ATTRIBUTE_CD_TENANT_ID))
                .cdUserId(parser.getAttributeValue(ATTRIBUTE_CD_USER_ID));
    }

    public static List<Cap> toCephCaps(RoleEnum roleEnum) {
        if (roleEnum == RoleEnum.TENANT_ADMIN) {
            return Arrays.asList(
                    new Cap(Cap.Type.USERS, Cap.Perm.READ_WRITE),
                    new Cap(Cap.Type.BUCKETS, Cap.Perm.READ_WRITE),
                    new Cap(Cap.Type.METADATA, Cap.Perm.READ_WRITE),
                    new Cap(Cap.Type.USAGE, Cap.Perm.READ)
            );
        }

        if (roleEnum == RoleEnum.PROVIDER_ADMIN) {
            return Arrays.asList(
                    new Cap(Cap.Type.USERS, Cap.Perm.READ),
                    new Cap(Cap.Type.USAGE, Cap.Perm.READ)
            );
        }

        //TODO other role mapping
        return Collections.emptyList();
    }

    public static RoleEnum fromCephCaps(List<Cap> caps) {
        Set<Cap> cephCaps = new HashSet<>(caps);
        for (RoleEnum role : RoleEnum.values()) {
            if (new HashSet<>(toCephCaps(role)).equals(cephCaps)) {
                return role;
            }
        }

        return RoleEnum.UNKNOWN;
    }

    public static String toCephCapsParam(List<Cap> caps) {
        List<String> capStrs = caps.stream().map(cap ->
                new StringBuilder().append(cap.getType().toString()).append("=").append(cap.getPerm().toString()).toString()
        ).collect(Collectors.toList());

        return String.join(";", capStrs);
    }


    public static OsisTenant toOsisTenant(User user) {
        return new OsisTenant()
                .name(toOsisTenantName(user))
                .active(user.getSuspended() == 0)
                .cdTenantIds(new DisplayNameRecordParser(user.getDisplayName()).getAttributeListValue(ATTRIBUTE_CD_TENANT_IDS))
                .tenantId(toOsisTenantId(user));
    }

    public static OsisUser toOsisUser(User user) {
        DisplayNameRecordParser parser = new DisplayNameRecordParser(user.getDisplayName());
        return new OsisUser()
                .active(user.getSuspended() == 0)
                .email(user.getEmail())
                .role(fromCephCaps(user.getCaps()))
                .tenantId(toOsisTenantId(user.getTenant()))
                .userId(user.getUserId())
                .canonicalUserId(toOsisCanonicalUserId(user.getTenant(), user.getUserId()))
                .displayName(parser.getAttributeValue(ATTRIBUTE_USERNAME))
                .cdTenantId(parser.getAttributeValue(ATTRIBUTE_CD_TENANT_ID))
                .cdUserId(parser.getAttributeValue(ATTRIBUTE_CD_USER_ID))
                .osisS3Credentials(user.getS3Credentials().stream().map(s3Credential -> toOsisS3Credential(user, s3Credential)).collect(Collectors.toList()));
    }

    public static OsisUsage toOsisUsage(List<BucketInfo> bi) {
        //totalBytes and availableBytes can't get from ceph.
        OsisUsage result = new OsisUsage();
        if (bi == null || bi.isEmpty()) {
            return result;
        }
        result.setBucketCount((long) bi.size());
        result.setObjectCount(bi.stream().map(BucketInfo::getUsage)
                .filter(Objects::nonNull)
                .map(BucketInfo.Usage::getRgwMain)
                .filter(Objects::nonNull)
                .mapToLong(BucketInfo.Usage.RgwMain::getNum_objects).sum());
        result.setUsedBytes(bi.stream().map(BucketInfo::getUsage)
                .filter(Objects::nonNull)
                .map(BucketInfo.Usage::getRgwMain)
                .filter(Objects::nonNull)
                .mapToLong(BucketInfo.Usage.RgwMain::getSize_kb_utilized).sum());
        return result;
    }

    private static String toOsisTenantName(User user) {
        if (user.getTenant().contains(DOUBLE_UNDER_SCORE)) {
            return user.getTenant().substring(0, user.getTenant().indexOf(DOUBLE_UNDER_SCORE));
        } else {
            return user.getTenant();
        }

    }

    public static String toCephTenantId(String osisTenantName, String cdTenantId) {
        return CephUtil.normalize(osisTenantName) + DOUBLE_UNDER_SCORE + CephUtil.normalize(cdTenantId);
    }

    public static String toCephTenantId(String osisTenantId) {
        return osisTenantId;
    }

    private static String toOsisTenantId(User user) {
        return user.getTenant();
    }

    private static String toOsisTenantId(String cephTenantId) {
        return cephTenantId;
    }

    private static String toOsisCanonicalUserId(String cephTenantId, String cephUserId) {
        return CephUtil.generateCephUid(cephTenantId, cephUserId);
    }

    static class DisplayNameRecordGenerator {
        List<String> attributes = new ArrayList<>();

        public DisplayNameRecordGenerator appendAttribute(String attrName, String attrValue) {
            if (StringUtils.isNotBlank(attrValue)) {
                attributes.add(attrName + ATTRIBUTE_EQUAL_SIGN + attrValue);
            }

            return this;
        }

        public DisplayNameRecordGenerator appendAttribute(String attrName, String... elements) {
            if (elements != null) {
                attributes.add(attrName + ATTRIBUTE_EQUAL_SIGN + String.join(ARRAY_SEPARATOR, elements));
            }

            return this;
        }

        public DisplayNameRecordGenerator appendAttribute(String attrName, List<String> elements) {
            if (elements != null) {
                attributes.add(attrName + ATTRIBUTE_EQUAL_SIGN + String.join(ARRAY_SEPARATOR, elements));
            }
            return this;
        }

        public String generate() {
            return String.join(ATTRIBUTE_SEPARATOR, attributes);
        }
    }

    static class DisplayNameRecordParser {

        Map<String, String> attrMap = new HashMap<>();

        public DisplayNameRecordParser(String displayName) {
            List<String> attributes = Arrays.asList(displayName.split(ATTRIBUTE_SEPARATOR));
            attributes.stream().forEach(attr -> {
                String[] kv = StringUtils.split(attr, ATTRIBUTE_EQUAL_SIGN);
                if (kv.length == 2) {
                    attrMap.put(kv[0], kv[1]);
                }
            });
        }

        public String getAttributeValue(String attrName) {
            return attrMap.get(attrName);
        }

        public List<String> getAttributeListValue(String attrName) {
            String value = attrMap.get(attrName);
            if (StringUtils.isNotBlank(value)) {
                return Arrays.asList(value.split(ARRAY_SEPARATOR));
            }

            return Collections.emptyList();
        }

    }

    public static OsisBucketMeta toOsisBucketMeta(BucketInfo bi) {
        return new OsisBucketMeta()
                .name(bi.getBucket())
                .userId(bi.getOwner());
    }
}
