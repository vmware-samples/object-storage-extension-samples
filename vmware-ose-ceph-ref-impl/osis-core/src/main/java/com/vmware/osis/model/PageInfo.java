/**
 *Copyright 2020 program was created by VMware.
 *SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.annotations.ApiModelProperty;
import javax.validation.constraints.*;

public class PageInfo {
  @NotNull
  private Long limit;

  @NotNull
  private Long offset;

  @NotNull
  private Long total;

  public PageInfo limit(Long limit) {
    this.limit = limit;
    return this;
  }

  /**
   * maxium number of the items in each page
   * @return limit
  */
  @ApiModelProperty(required = true, value = "maxium number of the items in each page")
  public Long getLimit() {
    return limit;
  }

  public void setLimit(Long limit) {
    this.limit = limit;
  }

  public PageInfo offset(Long offset) {
    this.offset = offset;
    return this;
  }

  /**
   * offset of the current page in the whole set of items
   * @return offset
  */
  @ApiModelProperty(required = true, value = "offset of the current page in the whole set of items")
  public Long getOffset() {
    return offset;
  }

  public void setOffset(Long offset) {
    this.offset = offset;
  }

  public PageInfo total(Long total) {
    this.total = total;
    return this;
  }

  /**
   * total number of the items
   * @return total
  */
  @ApiModelProperty(required = true, value = "total number of the items")
  public Long getTotal() {
    return total;
  }

  public void setTotal(Long total) {
    this.total = total;
  }


  @Override
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }

    PageInfo pageInfo = (PageInfo) o;

    if (limit != null ? !limit.equals(pageInfo.limit) : pageInfo.limit != null) {
      return false;
    }
    if (offset != null ? !offset.equals(pageInfo.offset) : pageInfo.offset != null) {
      return false;
    }
    return total != null ? total.equals(pageInfo.total) : pageInfo.total == null;
  }

  @Override
  public int hashCode() {
    int result = limit != null ? limit.hashCode() : 0;
    result = 31 * result + (offset != null ? offset.hashCode() : 0);
    result = 31 * result + (total != null ? total.hashCode() : 0);
    return result;
  }
}

