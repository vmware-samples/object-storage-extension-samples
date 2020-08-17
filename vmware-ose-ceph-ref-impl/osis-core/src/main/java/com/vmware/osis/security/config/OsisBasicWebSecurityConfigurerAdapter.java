/**
 * Copyright 2020 program was created by VMware.
 * SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.security.config;

import com.vmware.osis.ceph.security.CephUserDetailsService;
import com.vmware.osis.ceph.utils.CephUtil;
import com.vmware.osis.security.basic.BasicAuthentication;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

import static com.vmware.osis.security.jwt.AuthConstants.API_INFO;

@Configuration
@EnableWebSecurity
@ConditionalOnProperty(value = "security.jwt.enabled",
        havingValue = "false",
        matchIfMissing = false)
public class OsisBasicWebSecurityConfigurerAdapter extends WebSecurityConfigurerAdapter {

    @Autowired
    private BasicAuthentication authentication;

    @Autowired
    private CephUserDetailsService service;

    @Autowired
    public void configureGlobal(AuthenticationManagerBuilder auth) throws Exception {
        auth.userDetailsService(service).passwordEncoder(getPasswordEncoder());
        auth.eraseCredentials(true);
    }

    @Override
    public void configure(HttpSecurity http) throws Exception {
        http.cors().and().csrf().disable();
        http.authorizeRequests().antMatchers(API_INFO).permitAll();
        http.authorizeRequests().antMatchers(CephUtil.getLogoPath()).permitAll();
        http.authorizeRequests().anyRequest().authenticated();
        http.sessionManagement().sessionCreationPolicy(SessionCreationPolicy.NEVER);
        http.httpBasic().authenticationEntryPoint(authentication);
    }

    @Bean
    public PasswordEncoder getPasswordEncoder() {
        return new BCryptPasswordEncoder();
    }
}
