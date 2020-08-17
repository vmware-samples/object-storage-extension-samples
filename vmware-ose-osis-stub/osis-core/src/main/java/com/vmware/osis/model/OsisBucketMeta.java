/**
 *Copyright 2020 program was created by VMware.
 *SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.model;

import io.swagger.annotations.ApiModelProperty;

import javax.validation.Valid;
import javax.validation.constraints.NotNull;
import java.time.Instant;

public class OsisBucketMeta {
  @NotNull
  private String name;

  @Valid
  @NotNull
  private Instant creationDate;

  @NotNull
  private String userId;

  public OsisBucketMeta name(String name) {
    this.name = name;
    return this;
  }

  public OsisBucketMeta creationDate(Instant creationDate) {
    this.creationDate = creationDate;
    return this;
  }

  public OsisBucketMeta userId(String userId) {
    this.userId = userId;
    return this;
  }

  /**
   * bucket name
   * @return name
  */
  @ApiModelProperty(required = true, value = "bucket name")
  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  /**
   * bucket creation date
   * @return creationDate
  */
  @ApiModelProperty(required = true, value = "bucket creation date")
  public Instant getCreationDate() {
    return creationDate;
  }

  public void setCreationDate(Instant creationDate) {
    this.creationDate = creationDate;
  }

  /**
   * user id of bucket owner
   * @return userId
  */
  @ApiModelProperty(required = true, value = "user id of bucket owner")
  public String getUserId() {
    return userId;
  }

  public void setUserId(String userId) {
    this.userId = userId;
  }
}

