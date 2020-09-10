/**
 *Copyright 2020 VMware, Inc.
 *SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import javax.validation.constraints.*;

/**
 * a standard error object
 */
@ApiModel(description = "a standard error object")
public class OsisError {
  @NotNull
  @JsonProperty("code")
  private String code;

  @JsonProperty("message")
  private String message;

  public OsisError code(String code) {
    this.code = code;
    return this;
  }

  @ApiModelProperty(example = "E_BAD_REQUEST", required = true, value = "")
  public String getCode() {
    return code;
  }

  public void setCode(String code) {
    this.code = code;
  }

  public OsisError message(String message) {
    this.message = message;
    return this;
  }

  @ApiModelProperty(example = "invalid value for the property xyz.", value = "")
  public String getMessage() {
    return message;
  }

  public void setMessage(String message) {
    this.message = message;
  }
}

