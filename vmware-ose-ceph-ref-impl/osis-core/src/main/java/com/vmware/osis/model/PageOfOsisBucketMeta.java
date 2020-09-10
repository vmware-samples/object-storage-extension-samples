/**
 *Copyright 2020 VMware, Inc.
 *SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.model;

import java.util.ArrayList;
import java.util.List;

public class PageOfOsisBucketMeta implements Page<OsisBucketMeta> {
    private List<OsisBucketMeta> items;

    private PageInfo pageInfo;

    public PageOfOsisBucketMeta items(List<OsisBucketMeta> items) {
        this.items = items;
        return this;
    }

    public PageOfOsisBucketMeta addItem(OsisBucketMeta item) {
        if(this.items == null) {
            this.items = new ArrayList<>();
        }
        this.items.add(item);
        return this;
    }


    @Override
    public List<OsisBucketMeta> getItems() {
        return items;
    }

    public PageInfo getPageInfo() {
        return pageInfo;
    }

    @Override
    public void setItems(List<OsisBucketMeta> items) {
        this.items = items;
    }

    @Override
    public PageOfOsisBucketMeta pageInfo(PageInfo pageInfo) {
        this.pageInfo = pageInfo;
        return this;
    }

    @Override
    public void setPageInfo(PageInfo pageInfo) {
        this.pageInfo = pageInfo;
    }
}
