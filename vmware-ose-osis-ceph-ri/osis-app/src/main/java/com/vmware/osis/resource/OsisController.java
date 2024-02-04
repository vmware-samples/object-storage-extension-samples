/**
 * Copyright 2020 VMware, Inc.
 * SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.resource;

import com.vmware.osis.annotation.NotImplement;
import com.vmware.osis.model.*;
import com.vmware.osis.model.exception.*;
import com.vmware.osis.validation.Update;
import com.vmware.osis.service.OsisService;
import io.swagger.annotations.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;
import javax.validation.Valid;
import javax.validation.constraints.NotNull;
import java.util.Optional;


@Api(tags = "OSIS")
@RestController
public class OsisController {
    private static final Logger logger = LoggerFactory.getLogger(OsisController.class);


    @Autowired
    private OsisService osisService;

    /**
     * POST /api/v1/tenants/{tenantId}/users/{userId}/s3credentials : Create S3 credential for the platform user
     * Operation ID: createCredential&lt;br&gt; Create S3 credential for the platform user
     *
     * @param tenantId The ID of the tenant which the user belongs to (required)
     * @param userId   The ID of the user which the created S3 credential belongs to (required)
     * @return S3 credential is created for the user (status code 201)
     * or Bad Request (status code 400)
     */
    @ApiOperation(value = "Create S3 credential for the platform user", nickname = "createCredential", notes = "Operation ID: createCredential<br> Create S3 credential for the platform user ", response = OsisS3Credential.class, authorizations = {
            @Authorization(value = "basicAuth")
    }, tags = {"s3credential", "required",})
    @ApiResponses(value = {
            @ApiResponse(code = 201, message = "S3 credential is created for the user", response = OsisS3Credential.class),
            @ApiResponse(code = 400, message = "Bad Request", response = Error.class)})
    @ApiImplicitParams({
    })
    @PostMapping(value = "/api/v1/tenants/{tenantId}/users/{userId}/s3credentials",
            produces = "application/json")
    @ResponseStatus(HttpStatus.CREATED)
    public OsisS3Credential createCredential(
            @ApiParam(value = "The ID of the tenant which the user belongs to", required = true)
            @PathVariable("tenantId") String tenantId,
            @ApiParam(value = "The ID of the user which the created S3 credential belongs to", required = true)
            @PathVariable("userId") String userId) {
        return osisService.createS3Credential(tenantId, userId);
    }


    /**
     * POST /api/v1/tenants : Create a tenant in the platform
     * Operation ID: createTenant&lt;br&gt; Create a tenant in the platform. The platform decides whether to adopt the cd_tenand_id in request body as tenant_id. This means the platform could generate new tenant_id by itself for the new tenant. The tenant_id in request body is ignored.
     *
     * @param osisTenant Tenant to create in the platform (required)
     * @return A tenant is created (status code 201)
     * or Bad Request (status code 400)
     */
    @ApiOperation(value = "Create a tenant in the platform", nickname = "createTenant", notes = "Operation ID: createTenant<br> Create a tenant in the platform. The platform decides whether to adopt the cd_tenand_id in request body as tenant_id. This means the platform could generate new tenant_id by itself for the new tenant. The tenant_id in request body is ignored. ", response = OsisTenant.class, authorizations = {
            @Authorization(value = "basicAuth")
    }, tags = {"tenant", "required",})
    @ApiResponses(value = {
            @ApiResponse(code = 201, message = "A tenant is created", response = OsisTenant.class),
            @ApiResponse(code = 400, message = "Bad Request", response = Error.class)})
    @ApiImplicitParams({
    })
    @PostMapping(value = "/api/v1/tenants",
            produces = "application/json",
            consumes = "application/json")
    @ResponseStatus(HttpStatus.CREATED)
    public OsisTenant createTenant(
            @ApiParam(value = "Tenant to create in the platform", required = true)
            @Valid @RequestBody OsisTenant osisTenant) {
        return osisService.createTenant(osisTenant);
    }


    /**
     * POST /api/v1/tenants/{tenantId}/users : Create a user in the platform tenant
     * Operation ID: createUser&lt;br&gt; Create a user in the platform. The platform decides whether to adopt the cd_user_id in request body as canonical ID. This means the platform could generate new user_id by itself for the new user. The user_id in request body is ignored.
     *
     * @param tenantId The ID of the tenant which the created user belongs to (required)
     * @param osisUser User to create in the platform tenant. canonical_user_id is ignored. (required)
     * @return A user is created (status code 201)
     * or Bad Request (status code 400)
     */
    @ApiOperation(value = "Create a user in the platform tenant", nickname = "createUser", notes = "Operation ID: createUser<br> Create a user in the platform. The platform decides whether to adopt the cd_user_id in request body as canonical ID. This means the platform could generate new user_id by itself for the new user. The user_id in request body is ignored. ", response = OsisUser.class, authorizations = {
            @Authorization(value = "basicAuth")
    }, tags = {"user", "required",})
    @ApiResponses(value = {
            @ApiResponse(code = 201, message = "A user is created", response = OsisUser.class),
            @ApiResponse(code = 400, message = "Bad Request", response = Error.class)})
    @ApiImplicitParams({
    })
    @PostMapping(value = "/api/v1/tenants/{tenantId}/users",
            produces = "application/json",
            consumes = "application/json")
    @ResponseStatus(HttpStatus.CREATED)
    public OsisUser createUser(
            @ApiParam(value = "The ID of the tenant which the created user belongs to", required = true)
            @PathVariable("tenantId") String tenantId,
            @ApiParam(value = "User to create in the platform tenant. canonical_user_id is ignored.", required = true)
            @Valid @RequestBody OsisUser osisUser) {
        logger.info("create user");
        osisUser.setTenantId(tenantId);
        return osisService.createUser(osisUser);
    }


    /**
     * DELETE /api/v1/s3credentials/{accessKey} : Delete the S3 credential of the platform user
     * Operation ID: deleteCredential&lt;br&gt; Delete the S3 credential of the platform user. Parameters tenant_id and tenant_id are always in request; the platform decides whehter to use them.
     *
     * @param tenantId  The ID of the tenant which the user belongs to (required)
     * @param userId    The ID of the user which the deleted S3 credential belongs to (required)
     * @param accessKey The access key of the S3 credential to delete (required)
     * @return The S3 credential is deleted (status code 204)
     * or The optional API is not implemented (status code 501)
     */
    @ApiOperation(value = "Delete the S3 credential of the platform user", nickname = "deleteCredential", notes = "Operation ID: deleteCredential<br> Delete the S3 credential of the platform user. Parameters tenant_id and tenant_id are always in request; the platform decides whehter to use them. ", authorizations = {
            @Authorization(value = "basicAuth")
    }, tags = {"s3credential", "optional",})
    @ApiResponses(value = {
            @ApiResponse(code = 204, message = "The S3 credential is deleted"),
            @ApiResponse(code = 501, message = "The optional API is not implemented")})
    @ApiImplicitParams({
    })
    @DeleteMapping(value = "/api/v1/s3credentials/{accessKey}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteCredential(
            @NotNull @ApiParam(value = "The ID of the tenant which the user belongs to", required = true)
            @Valid @RequestParam(value = "tenant_id", required = true) String tenantId,
            @NotNull @ApiParam(value = "The ID of the user which the deleted S3 credential belongs to", required = true)
            @Valid @RequestParam(value = "user_id", required = true) String userId,
            @ApiParam(value = "The access key of the S3 credential to delete", required = true)
            @PathVariable("accessKey") String accessKey) {
        osisService.deleteS3Credential(tenantId, userId, accessKey);
    }


    /**
     * DELETE /api/v1/tenants/{tenantId} : Delete a tenant in the platform
     * Operation ID: deleteTenant&lt;br&gt; Delete a tenant in the platform
     *
     * @param tenantId  Tenant ID of the tenant to delete (required)
     * @param purgeData Purge data when the tenant is deleted (optional, default to false)
     * @return The tenant is deleted (status code 204)
     * or The optional API is not implemented (status code 501)
     */
    @ApiOperation(value = "Delete a tenant in the platform", nickname = "deleteTenant", notes = "Operation ID: deleteTenant<br> Delete a tenant in the platform ", authorizations = {
            @Authorization(value = "basicAuth")
    }, tags = {"tenant", "optional",})
    @ApiResponses(value = {
            @ApiResponse(code = 204, message = "The tenant is deleted"),
            @ApiResponse(code = 501, message = "The optional API is not implemented")})
    @ApiImplicitParams({
    })
    @DeleteMapping(value = "/api/v1/tenants/{tenantId}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteTenant(
            @ApiParam(value = "Tenant ID of the tenant to delete", required = true)
            @PathVariable("tenantId") String tenantId,
            @ApiParam(value = "Purge data when the tenant is deleted", defaultValue = "true")
            @Valid @RequestParam(value = "purge_data", required = false, defaultValue = "true")
            Boolean purgeData) {
        osisService.deleteTenant(tenantId, purgeData);
    }


    /**
     * DELETE /api/v1/tenants/{tenantId}/users/{userId} : Delete the user in the platform tenant
     * Operation ID: deleteUser&lt;br&gt; Delete the user in the platform tenant
     *
     * @param tenantId  The ID of the tenant which the deleted user belongs to (required)
     * @param userId    The ID of the user to delete (required)
     * @param purgeData Purge data when the user is deleted (optional, default to false)
     * @return The user is deleted (status code 204)
     */
    @ApiOperation(value = "Delete the user in the platform tenant", nickname = "deleteUser", notes = "Operation ID: deleteUser<br> Delete the user in the platform tenant ", authorizations = {
            @Authorization(value = "basicAuth")
    }, tags = {"user", "required",})
    @ApiResponses(value = {
            @ApiResponse(code = 204, message = "The user is deleted")})
    @ApiImplicitParams({
    })
    @DeleteMapping(value = "/api/v1/tenants/{tenantId}/users/{userId}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteUser(
            @ApiParam(value = "The ID of the tenant which the deleted user belongs to", required = true)
            @PathVariable("tenantId") String tenantId,
            @ApiParam(value = "The ID of the user to delete", required = true)
            @PathVariable("userId") String userId,
            @ApiParam(value = "Purge data when the user is deleted", defaultValue = "true")
            @Valid @RequestParam(value = "purge_data", required = false, defaultValue = "true")
            Boolean purgeData) {
        osisService.deleteUser(tenantId, userId, purgeData);
    }


    /**
     * GET /api/v1/bucket-list : Get the bucket list of the platform tenant
     * Operation ID: getBucketList&lt;br&gt; Get the bucket list of the platform tenant
     *
     * @param tenantId The ID of the tenant to get its bueckt list (required)
     * @param offset   The start index of buckets to return (optional)
     * @param limit    The maximum number of buckets to return (optional)
     * @return The bucket list of the platform tenant is returned (status code 200)
     * or The optional API is not implemented (status code 501)
     */
    @ApiOperation(value = "Get the bucket list of the platform tenant", nickname = "getBucketList", notes = "Operation ID: getBucketList<br> Get the bucket list of the platform tenant ", response = OsisBucketMeta.class, responseContainer = "List", authorizations = {
            @Authorization(value = "basicAuth")
    }, tags = {"bucketlist", "optional",})
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "The bucket list of the platform tenant is returned", response = OsisBucketMeta.class, responseContainer = "List"),
            @ApiResponse(code = 501, message = "The optional API is not implemented")})
    @ApiImplicitParams({
    })
    @GetMapping(value = "/api/v1/bucket-list",
            produces = "application/json")
    @NotImplement(name = OsisConstants.GET_BUCKET_LIST_API_CODE)
    public PageOfOsisBucketMeta getBucketList(
            @NotNull @ApiParam(value = "The ID of the tenant to get its bueckt list", required = true)
            @Valid @RequestParam(value = "tenant_id", required = true) String tenantId,
            @ApiParam(value = "The start index of buckets to return")
            @Valid @RequestParam(value = "offset", required = false, defaultValue = "0") long offset,
            @ApiParam(value = "The maximum number of buckets to return")
            @Valid @RequestParam(value = "limit", required = false, defaultValue = "100") long limit) {
        return osisService.getBucketList(tenantId, offset, limit);
    }


    /**
     * GET /api/v1/console : Get the console URI of the platform or platform tenant
     * Operation ID: getConsole&lt;br&gt; Get the console URI of the platform or platform tenant if tenantId is specified
     *
     * @param tenantId The ID of the tenant to get its console URI (optional)
     * @return The console URI is returned (status code 200)
     * or The optional API is not implemented (status code 501)
     */
    @ApiOperation(value = "Get the console URI of the platform or platform tenant", nickname = "getConsole", notes = "Operation ID: getConsole<br> Get the console URI of the platform or platform tenant if tenantId is specified ", response = String.class, authorizations = {
            @Authorization(value = "basicAuth")
    }, tags = {"console", "optional",})
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "The console URI is returned", response = String.class),
            @ApiResponse(code = 501, message = "The optional API is not implemented")})
    @ApiImplicitParams({
    })
    @GetMapping(value = "/api/v1/console",
            produces = "application/json")
    public String getConsole(
            @ApiParam(value = "The ID of the tenant to get its console URI")
            @Valid @RequestParam(value = "tenant_id", required = false) Optional<String> tenantId) {
        if (tenantId.isPresent()) {
            return osisService.getTenantConsoleUrl(tenantId.get());
        } else {
            return osisService.getProviderConsoleUrl();
        }
    }


    /**
     * GET /api/v1/s3credentials/{accessKey} : Get S3 credential of the platform user
     * Operation ID: createCredential&lt;br&gt; Get S3 credential of the platform user. Parameters tenant_id and tenant_id are always in request; the platform decides whehter to use them.
     *
     * @param tenantId  The ID of the tenant which the user belongs to (required)
     * @param userId    The ID of the user which the S3 credential belongs to (required)
     * @param accessKey The access key of the S3 credential to get (required)
     * @return The S3 credenital is returned (status code 200)
     * or Not Found (status code 404)
     */
    @ApiOperation(value = "Get S3 credential of the platform user", nickname = "getCredential", notes = "Operation ID: createCredential<br> Get S3 credential of the platform user. Parameters tenant_id and tenant_id are always in request; the platform decides whehter to use them. ", response = OsisS3Credential.class, authorizations = {
            @Authorization(value = "basicAuth")
    }, tags = {"s3credential", "required",})
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "The S3 credenital is returned", response = OsisS3Credential.class),
            @ApiResponse(code = 404, message = "Not Found", response = Object.class)})
    @ApiImplicitParams({
    })
    @GetMapping(value = "/api/v1/s3credentials/{accessKey}",
            produces = "application/json")
    public OsisS3Credential getCredential(
            @NotNull @ApiParam(value = "The ID of the tenant which the user belongs to", required = false)
            @Valid @RequestParam(value = "tenant_id", required = false) Optional<String> tenantId,
            @NotNull @ApiParam(value = "The ID of the user which the S3 credential belongs to", required = false)
            @Valid @RequestParam(value = "user_id", required = false) Optional<String> userId,
            @ApiParam(value = "The access key of the S3 credential to get", required = true)
            @PathVariable("accessKey") String accessKey) {
        return osisService.getS3Credential(accessKey);
    }


    /**
     * GET /api/info : Get the REST servcies information
     * Operation ID: getInfo&lt;br&gt; &#39;Get the information of the REST Services, including platform name, OSIS version and etc&#39;
     *
     * @return OK (status code 200)
     */
    @ApiOperation(value = "Get the REST servcies information", nickname = "getInfo", notes = "Operation ID: getInfo<br> 'Get the information of the REST Services, including platform name, OSIS version and etc' ", response = Information.class, tags = {"info", "required",})
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "OK", response = Information.class)})
    @ApiImplicitParams({
    })
    @GetMapping(value = "/api/info",
            produces = "application/json")
    @ResponseStatus(HttpStatus.OK)
    public Information getInfo(HttpServletRequest request) {
        StringBuffer url = request.getRequestURL();
        String domain = url.substring(0, url.lastIndexOf(request.getRequestURI()));
        logger.info(domain);
        return osisService.getInformation(domain);
    }


    /**
     * GET /api/v1/s3capabilities : Get S3 capabilities of the platform
     * Operation ID: getS3Capabilities&lt;br&gt; Get S3 capabilities of the platform
     *
     * @return S3 capabilities of the platform (status code 200)
     */
    @ApiOperation(value = "Get S3 capabilities of the platform", nickname = "getS3Capabilities", notes = "Operation ID: getS3Capabilities<br> Get S3 capabilities of the platform ", response = OsisS3Capabilities.class, authorizations = {
            @Authorization(value = "basicAuth")
    }, tags = {"usage", "required",})
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "S3 capabilities of the platform", response = OsisS3Capabilities.class)})
    @ApiImplicitParams({
    })
    @GetMapping(value = "/api/v1/s3capabilities",
            produces = "application/json")
    public OsisS3Capabilities getS3Capabilities() {
        return osisService.getS3Capabilities();
    }


    /**
     * GET /api/v1/tenants/{tenantId} : Get the tenant
     * Operation ID: getTenant&lt;br&gt; Get the tenant with tenant ID. The cd_tenant_id in the response indicates the mapping between Cloud Direct tenant and platform tenant. \&quot;
     *
     * @param tenantId Tenant ID to get the tenant from the platform (required)
     * @return The tenant is returned (status code 200)
     * or The tenant doesn&#39;t exist (status code 404)
     * or The optional API is not implemented (status code 501)
     */
    @ApiOperation(value = "Get the tenant", nickname = "getTenant", notes = "Operation ID: getTenant<br> Get the tenant with tenant ID. The cd_tenant_id in the response indicates the mapping between Cloud Direct tenant and platform tenant. \" ", response = OsisTenant.class, authorizations = {
            @Authorization(value = "basicAuth")
    }, tags = {"tenant", "optional",})
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "The tenant is returned", response = OsisTenant.class),
            @ApiResponse(code = 404, message = "The tenant doesn't exist"),
            @ApiResponse(code = 501, message = "The optional API is not implemented")})
    @ApiImplicitParams({
    })
    @GetMapping(value = "/api/v1/tenants/{tenantId}",
            produces = "application/json")
    public OsisTenant getTenant(
            @ApiParam(value = "Tenant ID to get the tenant from the platform", required = true)
            @PathVariable("tenantId") String tenantId) {
        return osisService.getTenant(tenantId);
    }


    /**
     * GET /api/v1/usage : Get the usage of the platform tenant or user
     * Operation ID: getUsage&lt;br&gt; Get the platform usage of global (without query parameter), tenant (with tenant_id) or user (only with user_id).
     *
     * @param tenantId The ID of the tenant to get its usage. &#39;tenant_id&#39; takes precedence over &#39;user_id&#39; to take effect if both are specified. (optional)
     * @param userId   The ID of the user to get its usage. &#39;tenant_id&#39; takes precedence over &#39;user_id&#39; to take effect if both are specified. (optional)
     * @return The usage of the tenant or user is returned (status code 200)
     * or The optional API is not implemented (status code 501)
     */
    @ApiOperation(value = "Get the usage of the platform tenant or user", nickname = "getUsage", notes = "Operation ID: getUsage<br> Get the platform usage of global (without query parameter), tenant (with tenant_id) or user (only with user_id). ", response = OsisUsage.class, authorizations = {
            @Authorization(value = "basicAuth")
    }, tags = {"usage", "optional",})
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "The usage of the tenant or user is returned", response = OsisUsage.class),
            @ApiResponse(code = 501, message = "The optional API is not implemented")})
    @ApiImplicitParams({
    })
    @GetMapping(value = "/api/v1/usage",
            produces = "application/json")
    public OsisUsage getUsage(
            @ApiParam(value = "The ID of the tenant to get its usage. 'tenant_id' takes precedence over 'user_id' to take effect if both are specified.")
            @Valid @RequestParam(value = "tenant_id", required = false) Optional<String> tenantId,
            @ApiParam(value = "The ID of the user to get its usage. 'tenant_id' takes precedence over 'user_id' to take effect if both are specified.")
            @Valid @RequestParam(value = "user_id", required = false) Optional<String> userId) {
        if (!tenantId.isPresent() && userId.isPresent()) {
            throw new BadRequestException("userId must be specified with associated tenantId!");
        }
        return osisService.getOsisUsage(tenantId, userId);
    }


    /**
     * GET /api/v1/users/{canonicalUserId} : Get the user with user canonical ID
     * Operation ID: getUserWithCanonicalID&lt;br&gt; Get the user with the user canonical ID
     *
     * @param canonicalUserId The canonical ID of the user to get (required)
     * @return The user is returned (status code 200)
     * or The tenant doesn&#39;t exist (status code 404)
     */
    @ApiOperation(value = "Get the user with user canonical ID", nickname = "getUserWithCanonicalID", notes = "Operation ID: getUserWithCanonicalID<br> Get the user with the user canonical ID ", response = OsisUser.class, authorizations = {
            @Authorization(value = "basicAuth")
    }, tags = {"user", "required",})
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "The user is returned", response = OsisUser.class),
            @ApiResponse(code = 404, message = "The tenant doesn't exist")})
    @ApiImplicitParams({
    })
    @GetMapping(value = "/api/v1/users/{canonicalUserId}",
            produces = "application/json")
    public OsisUser getUserWithCanonicalID(
            @ApiParam(value = "The canonical ID of the user to get", required = true)
            @PathVariable("canonicalUserId") String canonicalUserId) {
        return osisService.getUser(canonicalUserId);
    }


    /**
     * GET /api/v1/tenants/{tenantId}/users/{userId} : Get the user with user ID of the tenant
     * Operation ID: getUserWithId&lt;br&gt; Get the user with the user ID in the tenant. The cd_user_id in the response indicates the mapping between Cloud Direct user and platform user.
     *
     * @param tenantId The ID of the tenant which the user belongs to (required)
     * @param userId   The ID of the user to get (required)
     * @return The user is returned (status code 200)
     * or The tenant doesn&#39;t exist (status code 404)
     */
    @ApiOperation(value = "Get the user with user ID of the tenant", nickname = "getUserWithId", notes = "Operation ID: getUserWithId<br> Get the user with the user ID in the tenant. The cd_user_id in the response indicates the mapping between Cloud Direct user and platform user. ", response = OsisUser.class, authorizations = {
            @Authorization(value = "basicAuth")
    }, tags = {"user", "required",})
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "The user is returned", response = OsisUser.class),
            @ApiResponse(code = 404, message = "The tenant doesn't exist")})
    @ApiImplicitParams({
    })
    @GetMapping(value = "/api/v1/tenants/{tenantId}/users/{userId}",
            produces = "application/json")
    public OsisUser getUserWithId(
            @ApiParam(value = "The ID of the tenant which the user belongs to", required = true)
            @PathVariable("tenantId") String tenantId,
            @ApiParam(value = "The ID of the user to get", required = true)
            @PathVariable("userId") String userId) {
        return osisService.getUser(tenantId, userId);
    }


    /**
     * HEAD /api/v1/tenants/{tenantId} : Check whether the tenant exists
     * Operation ID: headTenant&lt;br&gt; Check whether the tenant exists
     *
     * @param tenantId Tenant ID to check on the platform (required)
     * @return The tenant exists (status code 200)
     * or The tenant doesn&#39;t exist (status code 404)
     */
    @ApiOperation(value = "Check whether the tenant exists", nickname = "headTenant", notes = "Operation ID: headTenant<br> Check whether the tenant exists ", authorizations = {
            @Authorization(value = "basicAuth")
    }, tags = {"tenant", "required",})
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "The tenant exists"),
            @ApiResponse(code = 404, message = "The tenant doesn't exist")})
    @ApiImplicitParams({
    })
    @RequestMapping(value = "/api/v1/tenants/{tenantId}",
            method = RequestMethod.HEAD)
    public Void headTenant(
            @ApiParam(value = "Tenant ID to check on the platform", required = true)
            @PathVariable("tenantId") String tenantId) {
        osisService.headTenant(tenantId);
        return null;
    }


    /**
     * HEAD /api/v1/tenants/{tenantId}/users/{userId} : Check whether the user exists
     * Operation ID: headUser&lt;br&gt; Check whether the user exists in the platform tenant
     *
     * @param tenantId The ID of the tenant which the user belongs to (required)
     * @param userId   The ID of the user to check (required)
     * @return The user exists (status code 200)
     * or The user doesn&#39;t exist (status code 404)
     * or The optional API is not implemented (status code 501)
     */
    @ApiOperation(value = "Check whether the user exists", nickname = "headUser", notes = "Operation ID: headUser<br> Check whether the user exists in the platform tenant ", authorizations = {
            @Authorization(value = "basicAuth")
    }, tags = {"user", "optional",})
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "The user exists"),
            @ApiResponse(code = 404, message = "The user doesn't exist"),
            @ApiResponse(code = 501, message = "The optional API is not implemented")})
    @ApiImplicitParams({
    })
    @RequestMapping(value = "/api/v1/tenants/{tenantId}/users/{userId}",
            method = RequestMethod.HEAD)
    public void headUser(
            @ApiParam(value = "The ID of the tenant which the user belongs to", required = true)
            @PathVariable("tenantId") String tenantId,
            @ApiParam(value = "The ID of the user to check", required = true)
            @PathVariable("userId") String userId) {
        osisService.headUser(tenantId, userId);

    }


    /**
     * GET /api/v1/tenants/{tenantId}/users/{userId}/s3credentials : List S3 credentials of the platform user
     * Operation ID: listCredentials&lt;br&gt; List S3 credentials of the platform user
     *
     * @param tenantId The ID of the tenant which the user belongs to (required)
     * @param userId   The ID of user which the S3 credenitials belong to (required)
     * @param offset   The start index of credentials to return (optional)
     * @param limit    Maximum number of credentials to return (optional)
     * @return S3 credentials of the platform user are returned (status code 200)
     */
    @ApiOperation(value = "List S3 credentials of the platform user", nickname = "listCredentials", notes = "Operation ID: listCredentials<br> List S3 credentials of the platform user ", response = PageOfS3Credentials.class, authorizations = {
            @Authorization(value = "basicAuth")
    }, tags = {"s3credential", "required",})
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "S3 credentials of the platform user are returned", response = PageOfS3Credentials.class)})
    @ApiImplicitParams({
    })
    @GetMapping(value = "/api/v1/tenants/{tenantId}/users/{userId}/s3credentials",
            produces = "application/json")
    public PageOfS3Credentials listCredentials(
            @ApiParam(value = "The ID of the tenant which the user belongs to", required = true)
            @PathVariable("tenantId") String tenantId,
            @ApiParam(value = "The ID of user which the S3 credenitials belong to", required = true)
            @PathVariable("userId") String userId,
            @ApiParam(value = "The start index of credentials to return")
            @Valid @RequestParam(value = "offset", required = false, defaultValue = "0") Long offset,
            @ApiParam(value = "Maximum number of credentials to return")
            @Valid @RequestParam(value = "limit", required = false, defaultValue = "100") Long limit) {


        return osisService.listS3Credentials(tenantId, userId, offset, limit);

    }


    /**
     * GET /api/v1/tenants : List tenants of platform
     * Operation ID: listTenants&lt;br&gt; List tenants of the platform
     *
     * @param offset The start index of tenants to return (optional)
     * @param limit  Maximum number of tenants to return (optional)
     * @return Tenants of the platform are returned (status code 200)
     */
    @ApiOperation(value = "List tenants of platform", nickname = "listTenants", notes = "Operation ID: listTenants<br> List tenants of the platform ", response = PageOfTenants.class, authorizations = {
            @Authorization(value = "basicAuth")
    }, tags = {"tenant", "required",})
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "Tenants of the platform are returned", response = PageOfTenants.class)})
    @ApiImplicitParams({
    })
    @GetMapping(value = "/api/v1/tenants",
            produces = "application/json")
    public PageOfTenants listTenants(
            @ApiParam(value = "The start index of tenants to return")
            @Valid @RequestParam(value = "offset", required = false, defaultValue = "0") Long offset,
            @ApiParam(value = "Maximum number of tenants to return")
            @Valid @RequestParam(value = "limit", required = false, defaultValue = "100") Long limit) {
        return osisService.listTenants(offset, limit);
    }


    /**
     * GET /api/v1/tenants/{tenantId}/users : List users of the platform tenant
     * Operation ID: listUsers&lt;br&gt; List users of the platform tenant
     *
     * @param tenantId The ID of the tenant which the listed users belongs to (required)
     * @param offset   The start index of users to return (optional)
     * @param limit    Maximum number of users to return (optional)
     * @return Users of the platform tenant are returned (status code 200)
     */
    @ApiOperation(value = "List users of the platform tenant", nickname = "listUsers", notes = "Operation ID: listUsers<br> List users of the platform tenant ", response = PageOfUsers.class, authorizations = {
            @Authorization(value = "basicAuth")
    }, tags = {"user", "required",})
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "Users of the platform tenant are returned", response = PageOfUsers.class)})
    @ApiImplicitParams({
    })
    @GetMapping(value = "/api/v1/tenants/{tenantId}/users",
            produces = "application/json")
    public PageOfUsers listUsers(
            @ApiParam(value = "The ID of the tenant which the listed users belongs to", required = true)
            @PathVariable("tenantId") String tenantId,
            @ApiParam(value = "The start index of users to return")
            @Valid @RequestParam(value = "offset", required = false, defaultValue = "0") long offset,
            @ApiParam(value = "Maximum number of users to return")
            @Valid @RequestParam(value = "limit", required = false, defaultValue = "100") long limit) {
        return osisService.listUsers(tenantId, offset, limit);
    }


    /**
     * PATCH /api/v1/s3credentials/{accessKey} : Enable or disable S3 credential for the platform user
     * Operation ID: updateCredentialStatus&lt;br&gt; Enabled or disable S3 credential for the platform user. Parameters tenant_id and tenant_id are always in request; the platform decides whehter to use them.
     *
     * @param tenantId         The ID of the tenant which the user belongs to (required)
     * @param userId           The ID of the user which the status updated S3 credential belongs to (required)
     * @param accessKey        The access key of the S3 credential to update status (required)
     * @param osisS3Credential The S3 credential containing the status to update. Only property &#39;active&#39; takes effect (required)
     * @return The status of the S3 credential is updated (status code 200)
     * or Bad Request (status code 400)
     * or The optional API is not implemented (status code 501)
     */
    @ApiOperation(value = "Enable or disable S3 credential for the platform user", nickname = "updateCredentialStatus", notes = "Operation ID: updateCredentialStatus<br> Enabled or disable S3 credential for the platform user. Parameters tenant_id and tenant_id are always in request; the platform decides whehter to use them. ", response = OsisS3Credential.class, authorizations = {
            @Authorization(value = "basicAuth")
    }, tags = {"s3credential", "optional",})
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "The status of the S3 credential is updated", response = OsisS3Credential.class),
            @ApiResponse(code = 400, message = "Bad Request", response = Error.class),
            @ApiResponse(code = 501, message = "The optional API is not implemented")})
    @ApiImplicitParams({
    })
    @PatchMapping(value = "/api/v1/s3credentials/{accessKey}",
            produces = "application/json",
            consumes = "application/json")
    @NotImplement(name = OsisConstants.UPDATE_CREDENTIAL_STATUS_API_CODE)
    public OsisS3Credential updateCredentialStatus(
            @NotNull @ApiParam(value = "The ID of the tenant which the user belongs to", required = true)
            @Valid @RequestParam(value = "tenant_id", required = true) String tenantId,
            @NotNull @ApiParam(value = "The ID of the user which the status updated S3 credential belongs to", required = true)
            @Valid @RequestParam(value = "user_id", required = true) String userId,
            @ApiParam(value = "The access key of the S3 credential to update status", required = true)
            @PathVariable("accessKey") String accessKey,
            @ApiParam(value = "The S3 credential containing the status to update. Only property 'active' takes effect", required = true)
            @Valid @RequestBody OsisS3Credential osisS3Credential) {
        throw new NotImplementedException();
    }


    /**
     * PATCH /api/v1/tenants/{tenantId} : Enable or disable tenant of the platform
     * Operation ID: updateTenantStatus&lt;br&gt; Update status of the tenant in the platform
     *
     * @param tenantId   Tenant ID of the tenant to update status (required)
     * @param osisTenant Tenant status to update in the platform. Only property &#39;active&#39; takes effect (required)
     * @return The tenant status is updated (status code 200)
     * or Bad Request (status code 400)
     */
    @ApiOperation(value = "Enable or disable tenant of the platform", nickname = "updateTenantStatus", notes = "Operation ID: updateTenantStatus<br> Update status of the tenant in the platform ", response = OsisTenant.class, authorizations = {
            @Authorization(value = "basicAuth")
    }, tags = {"tenant", "required",})
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "The tenant status is updated", response = OsisTenant.class),
            @ApiResponse(code = 400, message = "Bad Request", response = Error.class)})
    @ApiImplicitParams({
    })
    @PatchMapping(value = "/api/v1/tenants/{tenantId}",
            produces = "application/json",
            consumes = "application/json")
    public OsisTenant updateTenantStatus(
            @ApiParam(value = "Tenant ID of the tenant to update status", required = true)
            @PathVariable("tenantId") String tenantId,
            @ApiParam(value = "Tenant status to update in the platform. Only property 'active' takes effect", required = true)
            @Valid @RequestBody OsisTenant osisTenant) {
        return osisService.updateTenant(tenantId, osisTenant);
    }


    /**
     * PATCH /api/v1/tenants/{tenantId}/users/{userId} : Enable or disable status in the tenant
     * Operation ID: updateUserStatus&lt;br&gt; Update status of the user in the platform tenant
     *
     * @param tenantId The ID of the tenant which the user to update belongs to (required)
     * @param userId   The ID of the user to update (required)
     * @param osisUser User status to update in the platform tenant. Only property &#39;active&#39; takes effect (required)
     * @return The user status is updated (status code 201)
     * or Bad Request (status code 400)
     */
    @ApiOperation(value = "Enable or disable status in the tenant", nickname = "updateUserStatus", notes = "Operation ID: updateUserStatus<br> Update status of the user in the platform tenant ", response = OsisUser.class, authorizations = {
            @Authorization(value = "basicAuth")
    }, tags = {"user", "required",})
    @ApiResponses(value = {
            @ApiResponse(code = 201, message = "The user status is updated", response = OsisUser.class),
            @ApiResponse(code = 400, message = "Bad Request", response = Error.class)})
    @ApiImplicitParams({
    })
    @PatchMapping(value = "/api/v1/tenants/{tenantId}/users/{userId}",
            produces = "application/json",
            consumes = "application/json")
    public OsisUser updateUserStatus(
            @ApiParam(value = "The ID of the tenant which the user to update belongs to", required = true)
            @PathVariable("tenantId") String tenantId,
            @ApiParam(value = "The ID of the user to update", required = true)
            @PathVariable("userId") String userId,
            @ApiParam(value = "User status to update in the platform tenant. Only property 'active' takes effect", required = true)
            @Validated(value = Update.class) @RequestBody OsisUser osisUser) {
        return osisService.updateUser(tenantId, userId, osisUser);
    }

    /**
     * GET /api/v1/tenants/query : Query tenants of platform
     * Operation ID: queryTenants&lt;br&gt; Query tenants of the platform
     *
     * @param offset The start index of tenants to return (optional)
     * @param limit  Maximum number of tenants to return (optional)
     * @param filter The conditions to query platform tenants (optional)
     * @return Tenants of the platform are returned (status code 200)
     */
    @ApiOperation(value = "Query tenants of platform", nickname = "queryTenants", notes = "Operation ID: queryTenants<br> Query tenants of the platform ", response = PageOfTenants.class, authorizations = {
            @Authorization(value = "basicAuth")
    }, tags = {"tenant", "required",})
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "Tenants of the platform are returned", response = PageOfTenants.class)})
    @ApiImplicitParams({
    })
    @GetMapping(value = "/api/v1/tenants/query",
            produces = "application/json")
    public PageOfTenants queryTenants(
            @ApiParam(value = "The start index of tenants to return")
            @Valid @RequestParam(value = "offset", required = false, defaultValue = "0") long offset,
            @ApiParam(value = "Maximum number of tenants to return")
            @Valid @RequestParam(value = "limit", required = false, defaultValue = "100") long limit,
            @ApiParam(value = "The conditions to query platform tenants")
            @Valid @RequestParam(value = "filter", required = false) String filter) {
        return osisService.queryTenants(offset, limit, filter);
    }


    /**
     * GET /api/v1/users/query : Query users of the platform tenant
     * Operation ID: queryUsers&lt;br&gt; Query users of the platform tenant
     *
     * @param offset The start index of users to return (optional)
     * @param limit  Maximum number of users to return (optional)
     * @param filter The conditions to query platform users (optional)
     * @return Users of the platform tenant are returned (status code 200)
     */
    @ApiOperation(value = "Query users of the platform tenant", nickname = "queryUsers", notes = "Operation ID: queryUsers<br> Query users of the platform tenant ", response = PageOfUsers.class, authorizations = {
            @Authorization(value = "basicAuth")
    }, tags = {"user", "required",})
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "Users of the platform tenant are returned", response = PageOfUsers.class)})
    @ApiImplicitParams({
    })
    @GetMapping(value = "/api/v1/users/query",
            produces = "application/json")
    public PageOfUsers queryUsers(
            @ApiParam(value = "The start index of users to return")
            @Valid @RequestParam(value = "offset", required = false, defaultValue = "0") long offset,
            @ApiParam(value = "Maximum number of users to return")
            @Valid @RequestParam(value = "limit", required = false, defaultValue = "100") long limit,
            @ApiParam(value = "The conditions to query platform users")
            @Valid @RequestParam(value = "filter", required = false) String filter) {

        return osisService.queryUsers(offset, limit, filter);
    }

    /**
     * GET /api/v1/s3credentials/query : Query S3 credentials of the platform user
     * Operation ID: queryCredentials&lt;br&gt; Query S3 credentials of the platform user
     *
     * @param offset The start index of credentials to return (optional)
     * @param limit  Maximum number of credentials to return (optional)
     * @param filter The conditions to query platform users (optional)
     * @return S3 credentials of the platform user are returned (status code 200)
     */
    @ApiOperation(value = "Query S3 credentials of the platform user", nickname = "queryCredentials", notes = "Operation ID: queryCredentials<br> Query S3 credentials of the platform user ", response = PageOfS3Credentials.class, authorizations = {
            @Authorization(value = "basicAuth")
    }, tags = {"s3credential", "required",})
    @ApiResponses(value = {
            @ApiResponse(code = 200, message = "S3 credentials of the platform user are returned", response = PageOfS3Credentials.class)})
    @ApiImplicitParams({
    })
    @GetMapping(value = "/api/v1/s3credentials/query",
            produces = "application/json")
    public PageOfS3Credentials queryCredentials(
            @ApiParam(value = "The start index of credentials to return")
            @Valid @RequestParam(value = "offset", required = false, defaultValue = "0") long offset,
            @ApiParam(value = "Maximum number of credentials to return")
            @Valid @RequestParam(value = "limit", required = false, defaultValue = "100") long limit,
            @ApiParam(value = "The conditions to query platform users")
            @Valid @RequestParam(value = "filter", required = false) String filter) {
        return this.osisService.queryS3Credentials(offset, limit, filter);
    }

    @GetMapping(value = "/api/v1/bucket-logging-id",
            produces = "application/json")
    @NotImplement(name = OsisConstants.GET_BUCKET_ID_LOGGING_API_CODE)
    public OsisBucketLoggingId getBucketLoggingId() {
        throw new NotImplementedException();
    }

    @GetMapping(value = "/api/v1/anonymous-user",
            produces = "application/json")
    @NotImplement(name = OsisConstants.GET_ANONYMOUS_USER_API_CODE)
    public OsisUser getAnonymousUser() {
        throw new NotImplementedException();
    }

    @PostMapping(value = "/api/admin-apis", produces = "application/json")
    public OsisCaps updateOsisCaps(@RequestBody OsisCaps osisCaps) {
        return this.osisService.updateOsisCaps(osisCaps);
    }
}

