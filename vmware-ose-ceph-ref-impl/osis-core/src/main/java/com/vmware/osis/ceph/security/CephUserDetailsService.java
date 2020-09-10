/**
 * Copyright 2020 VMware, Inc.
 * SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.ceph.security;

import com.vmware.osis.ceph.AppEnv;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Component;

@Component
public class CephUserDetailsService implements UserDetailsService {

    @Autowired
    private AppEnv appEnv;

    @Override
    public UserDetails loadUserByUsername(String username) {
        if (username == null || !username.equals(appEnv.getRgwAccessKey())) {
            throw new UsernameNotFoundException(username);
        }
        return new CephUserDetails(appEnv.getRgwAccessKey(), appEnv.getRgwSecretKey());
    }
}
