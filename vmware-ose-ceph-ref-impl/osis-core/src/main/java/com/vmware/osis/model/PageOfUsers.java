/**
 *Copyright 2020 program was created by VMware.
 *SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.annotations.ApiModelProperty;

import javax.validation.Valid;
import java.util.ArrayList;
import java.util.List;

public class PageOfUsers implements Page<OsisUser> {
    @Valid
    private List<OsisUser> items = null;

    private PageInfo pageInfo;

    public PageOfUsers items(List<OsisUser> items) {
        this.items = items;
        return this;
    }

    public PageOfUsers addItemsItem(OsisUser itemsItem) {
        if (this.items == null) {
            this.items = new ArrayList<>();
        }
        this.items.add(itemsItem);
        return this;
    }

    /**
     * Get items
     *
     * @return items
     */
    @ApiModelProperty(value = "")
    public List<OsisUser> getItems() {
        return items;
    }

    public void setItems(List<OsisUser> items) {
        this.items = items;
    }

    public PageOfUsers pageInfo(PageInfo pageInfo) {
        this.pageInfo = pageInfo;
        return this;
    }

    /**
     * Get pageInfo
     *
     * @return pageInfo
     */
    @ApiModelProperty(value = "")
    public PageInfo getPageInfo() {
        return pageInfo;
    }

    public void setPageInfo(PageInfo pageInfo) {
        this.pageInfo = pageInfo;
    }

}
