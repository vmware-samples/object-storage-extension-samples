/**
 *Copyright 2020 VMware, Inc.
 *SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.model.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

public class NotImplementedException extends ResponseStatusException {

    public NotImplementedException() {
        super(HttpStatus.NOT_IMPLEMENTED, "The interface is not implemented.");
    }
}
