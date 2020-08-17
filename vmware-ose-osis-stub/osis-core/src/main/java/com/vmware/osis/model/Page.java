/**
 *Copyright 2020 program was created by VMware.
 *SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.model;

import java.util.List;

public interface Page<T> {

    List<T> getItems();

    void setItems(List<T> items);

    Page<T> pageInfo(PageInfo pageInfo);

    void setPageInfo(PageInfo pageInfo);
}
