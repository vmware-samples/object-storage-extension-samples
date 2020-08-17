/**
 *Copyright 2020 program was created by VMware.
 *SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.model;

import io.swagger.annotations.ApiModelProperty;

import javax.validation.constraints.NotNull;

public class OsisUsage {
    @NotNull
    private Long bucketCount;

    @NotNull
    private Long objectCount;

    @NotNull
    private Long totalBytes;

    @NotNull
    private Long availableBytes;

    @NotNull
    private Long usedBytes;

    public OsisUsage() {
        totalBytes = 0L;
        availableBytes = 0L;
        usedBytes = 0L;
        bucketCount = 0L;
        objectCount = 0L;
    }

    public OsisUsage bucketCount(Long bucketCount) {
        this.bucketCount = bucketCount;
        return this;
    }

    /**
     * bucket count of tenant or user
     *
     * @return bucketCount
     */
    @ApiModelProperty(example = "532", required = true, value = "bucket count of tenant or user")
    public Long getBucketCount() {
        return bucketCount;
    }

    public void setBucketCount(Long bucketCount) {
        this.bucketCount = bucketCount;
    }

    public OsisUsage objectCount(Long objectCount) {
        this.objectCount = objectCount;
        return this;
    }

    /**
     * object count of tenant or user
     *
     * @return objectCount
     */
    @ApiModelProperty(example = "298635", required = true, value = "object count of tenant or user")
    public Long getObjectCount() {
        return objectCount;
    }

    public void setObjectCount(Long objectCount) {
        this.objectCount = objectCount;
    }

    public OsisUsage totalBytes(Long totalBytes) {
        this.totalBytes = totalBytes;
        return this;
    }

    /**
     * total storage bytes of tenant or user
     *
     * @return totalBytes
     */
    @ApiModelProperty(example = "80948230763", required = true, value = "total storage bytes of tenant or user")
    public Long getTotalBytes() {
        return totalBytes;
    }

    public void setTotalBytes(Long totalBytes) {
        this.totalBytes = totalBytes;
    }

    public OsisUsage avaialbleBytes(Long avaialbleBytes) {
        this.availableBytes = avaialbleBytes;
        return this;
    }

    /**
     * available storage bytes of tenant or user
     *
     * @return avaialbleBytes
     */
    @ApiModelProperty(example = "48193854929", required = true, value = "available storage bytes of tenant or user")
    public Long getAvailableBytes() {
        return availableBytes;
    }

    public void setAvailableBytes(Long availableBytes) {
        this.availableBytes = availableBytes;
    }

    public OsisUsage usedBytes(Long usedBytes) {
        this.usedBytes = usedBytes;
        return this;
    }

    /**
     * used storage bytes of tenant or user
     *
     * @return usedBytes
     */
    @ApiModelProperty(example = "32754375834", required = true, value = "used storage bytes of tenant or user")
    public Long getUsedBytes() {
        return usedBytes;
    }

    public void setUsedBytes(Long usedBytes) {
        this.usedBytes = usedBytes;
    }
}

