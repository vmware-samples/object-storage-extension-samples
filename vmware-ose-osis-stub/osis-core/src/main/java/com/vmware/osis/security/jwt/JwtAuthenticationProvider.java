/**
 * Copyright 2020 program was created by VMware.
 * SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.security.jwt;

import com.vmware.osis.platform.AppEnv;
import com.vmware.osis.security.jwt.model.JwtAuthenticationToken;
import com.vmware.osis.security.jwt.model.RawAccessToken;
import com.vmware.osis.security.jwt.model.UserContext;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jws;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.AuthenticationProvider;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;

import java.util.List;
import java.util.stream.Collectors;

import static com.vmware.osis.security.jwt.AuthConstants.CLAIMS_SCOPES;

public class JwtAuthenticationProvider implements AuthenticationProvider {
    private final AppEnv appEnv;

    @Autowired
    public JwtAuthenticationProvider(AppEnv appEnv) {
        this.appEnv = appEnv;
    }

    @Override
    public Authentication authenticate(Authentication authentication) {
        RawAccessToken rawAccessToken = (RawAccessToken) authentication.getCredentials();

        Jws<Claims> jwsClaims = rawAccessToken.parseClaims(appEnv.getTokenSigningKey());
        String subject = jwsClaims.getBody().getSubject();
        List<String> scopes = jwsClaims.getBody().get(CLAIMS_SCOPES, List.class);
        List<GrantedAuthority> authorities = scopes.stream()
                .map(SimpleGrantedAuthority::new)
                .collect(Collectors.toList());

        UserContext context = UserContext.create(subject, authorities);

        return new JwtAuthenticationToken(context, context.getAuthorities());
    }

    @Override
    public boolean supports(Class<?> authentication) {
        return (JwtAuthenticationToken.class.isAssignableFrom(authentication));
    }
}
