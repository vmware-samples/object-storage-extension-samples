/**
 *Copyright 2020 program was created by VMware.
 *SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.annotations.ApiModelProperty;

import java.util.ArrayList;
import java.util.List;

public class OsisTenant {

//  @NotNull
  private boolean active;

//  @NotNull
  private String name;

//  @NotNull
  private String tenantId;

  private List<String> cdTenantIds;



  public OsisTenant active(boolean active) {
    this.active = active;
    return this;
  }

  public boolean getActive() {
    return this.active;
  }

  public OsisTenant name(String name) {
    this.name = name;
    return this;
  }

  /**
   * tenant name
   * @return name
  */
  @ApiModelProperty(example = "ACME", required = true, value = "tenant name")
  public String getName() {
    return name;
  }

  public void setName(String name) {
    this.name = name;
  }

  /**
   * tenant status
   * @return active
  */

  public OsisTenant tenantId(String tenantId) {
    this.tenantId = tenantId;
    return this;
  }

  /**
   * tenant id
   * @return tenantId
  */
  @ApiModelProperty(example = "d290f1ee-6c54-4b01-90e6-d701748f0851", required = true, value = "tenant id")
  public String getTenantId() {
    return tenantId;
  }

  public void setTenantId(String tenantId) {
    this.tenantId = tenantId;
  }

  public OsisTenant cdTenantIds(List<String> cdTenantIds) {
    this.cdTenantIds= cdTenantIds;
    return this;
  }

  public OsisTenant addCdTenantId(String cdTenantId) {
    if (this.cdTenantIds == null) {
      this.cdTenantIds = new ArrayList<>();
    }
    this.cdTenantIds.add(cdTenantId);
    return this;
  }

  /**
   * Cloud Director tenant id
   * @return cdTenantIds
  */
  @ApiModelProperty(example = "8daca9a9-5b11-4f63-9c52-953a2ef77739", required = true, value = "Cloud Director tenant id")
  public List<String> getCdTenantIds() {
    return cdTenantIds;
  }

  public void setCdTenantIds(List<String> cdTenantIds) {
    this.cdTenantIds = cdTenantIds;
  }


  @Override
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }

    OsisTenant that = (OsisTenant) o;

    if (active != that.active) {
      return false;
    }
    if (name != null ? !name.equals(that.name) : that.name != null) {
      return false;
    }
    if (tenantId != null ? !tenantId.equals(that.tenantId) : that.tenantId != null) {
      return false;
    }
    return cdTenantIds != null ? cdTenantIds.equals(that.cdTenantIds) : that.cdTenantIds == null;
  }

  @Override
  public int hashCode() {
    int result = (active ? 1 : 0);
    result = 31 * result + (name != null ? name.hashCode() : 0);
    result = 31 * result + (tenantId != null ? tenantId.hashCode() : 0);
    result = 31 * result + (cdTenantIds != null ? cdTenantIds.hashCode() : 0);
    return result;
  }
}

