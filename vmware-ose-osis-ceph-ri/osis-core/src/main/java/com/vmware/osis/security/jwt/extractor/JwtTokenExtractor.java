/**
 *Copyright 2020 VMware, Inc.
 *SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.security.jwt.extractor;

public interface JwtTokenExtractor {
    String extract(String payload);
}
