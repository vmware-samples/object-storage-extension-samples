/**
 *Copyright 2020 VMware, Inc.
 *SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.model;

import io.swagger.annotations.ApiModelProperty;

public class InformationServices {
  private String s3;

  private String iam;

  public InformationServices s3(String s3) {
    this.s3 = s3;
    return this;
  }

  public InformationServices iam(String iam) {
    this.iam = iam;
    return this;
  }

  /**
   * S3 URL of the storage platform
   * @return s3
  */
  @ApiModelProperty(example = "https://s3.ceph.ose.vmware.com", value = "S3 URL of the storage platform")
  public String getS3() {
    return s3;
  }

  public void setS3(String s3) {
    this.s3 = s3;
  }

  /**
   * IAM URL of the storage platform
   * @return iam
  */
  @ApiModelProperty(example = "https://iam.ceph.ose.vmware.com", value = "IAM URL of the storage platform")
  public String getIam() {
    return iam;
  }

  public void setIam(String iam) {
    this.iam = iam;
  }
}

