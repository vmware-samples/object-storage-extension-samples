/**
 *Copyright 2020 program was created by VMware.
 *SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.security.jwt.extractor;

public interface JwtTokenExtractor {
    String extract(String payload);
}
