/**
 *Copyright 2020 VMware, Inc.
 *SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.security.jwt;

import com.vmware.osis.platform.AppEnv;
import com.vmware.osis.security.jwt.model.AccessToken;
import com.vmware.osis.security.jwt.model.JwtToken;
import com.vmware.osis.security.jwt.model.Scopes;
import com.vmware.osis.security.jwt.model.UserContext;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import org.apache.commons.lang3.StringUtils;

import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.Arrays;
import java.util.Date;
import java.util.UUID;
import java.util.stream.Collectors;

import static com.vmware.osis.security.jwt.AuthConstants.CLAIMS_SCOPES;

public class JwtTokenFactory {
    private final AppEnv appEnv;

    public JwtTokenFactory(AppEnv appEnv) {
        this.appEnv = appEnv;
    }

    public AccessToken createAccessJwtToken(UserContext userContext) {
        if (StringUtils.isBlank(userContext.getUsername()))
            throw new IllegalArgumentException("Username is required to create token.");

        if (userContext.getAuthorities() == null || userContext.getAuthorities().isEmpty())
            throw new IllegalArgumentException("The login user has no privileges");

        Claims claims = Jwts.claims().setSubject(userContext.getUsername());
        claims.put(CLAIMS_SCOPES, userContext.getAuthorities().stream().map(Object::toString).collect(Collectors.toList()));

        LocalDateTime currentTime = LocalDateTime.now();

        String token = Jwts.builder()
                .setClaims(claims)
                .setIssuer(appEnv.getTokenIssuer())
                .setIssuedAt(Date.from(currentTime.atZone(ZoneId.systemDefault()).toInstant()))
                .setExpiration(Date.from(currentTime
                        .plusMinutes(appEnv.getAccessTokenExpirationTime())
                        .atZone(ZoneId.systemDefault()).toInstant()))
                .signWith(SignatureAlgorithm.HS512, appEnv.getTokenSigningKey())
                .compact();

        return new AccessToken(token, claims);
    }

    public JwtToken createRefreshToken(UserContext userContext) {
        if (StringUtils.isBlank(userContext.getUsername())) {
            throw new IllegalArgumentException("Username is required to create token.");
        }

        LocalDateTime currentTime = LocalDateTime.now();

        Claims claims = Jwts.claims().setSubject(userContext.getUsername());
        claims.put(CLAIMS_SCOPES, Arrays.asList(Scopes.REFRESH_TOKEN.authority()));


        String token = Jwts.builder()
                .setClaims(claims)
                .setIssuer(appEnv.getTokenIssuer())
                .setId(UUID.randomUUID().toString())
                .setIssuedAt(Date.from(currentTime.atZone(ZoneId.systemDefault()).toInstant()))
                .setExpiration(Date.from(currentTime
                        .plusMinutes(appEnv.getRefreshTokenExpirationTime())
                        .atZone(ZoneId.systemDefault()).toInstant()))
                .signWith(SignatureAlgorithm.HS512, appEnv.getTokenSigningKey())
                .compact();

        return new AccessToken(token, claims);
    }
}
