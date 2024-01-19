/**
 * Copyright 2020 VMware, Inc.
 * SPDX-License-Identifier: Apache License 2.0
 */

package com.vmware.osis.model;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import io.swagger.annotations.ApiModelProperty;

import java.util.*;

public class OsisS3Capabilities {

    private Map<String, OsisS3CapabilitiesExclusions> exclusions = new HashMap<>();


    public OsisS3Capabilities exclusions(Map<String, OsisS3CapabilitiesExclusions> exclusions) {

        this.exclusions = exclusions;
        return this;
    }

    public OsisS3Capabilities putExclusionsItem(String key, OsisS3CapabilitiesExclusions exclusionsItem) {
        this.exclusions.put(key, exclusionsItem);
        return this;
    }

    public Map<String, OsisS3CapabilitiesExclusions> getExclusions() {
        return exclusions;
    }


    public void setExclusions(Map<String, OsisS3CapabilitiesExclusions> exclusions) {
        this.exclusions = exclusions;
    }

    @Override
    public boolean equals(java.lang.Object o) {
        if (this == o) {
            return true;
        }
        if (o == null || getClass() != o.getClass()) {
            return false;
        }
        OsisS3Capabilities osisS3Capabilities = (OsisS3Capabilities) o;
        return Objects.equals(this.exclusions, osisS3Capabilities.exclusions);
    }

    @Override
    public int hashCode() {
        return Objects.hash(exclusions);
    }


    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append("class OsisS3Capabilities {\n");
        sb.append("    exclusions: ").append(toIndentedString(exclusions)).append("\n");
        sb.append("}");
        return sb.toString();
    }

    /**
     * Convert the given object to string with each line indented by 4 spaces
     * (except the first line).
     */
    private String toIndentedString(java.lang.Object o) {
        if (o == null) {
            return "null";
        }
        return o.toString().replace("\n", "\n    ");
    }

    @JsonInclude(JsonInclude.Include.NON_NULL)
    public static class OsisS3CapabilitiesExclusions {

        public static final String JSON_PROPERTY_ALL = "all";
        private boolean all = false;

        public static final String JSON_PROPERTY_BY_PARAMS = "by_params";
        private List<String> byParams = null;

        public static final String JSON_PROPERTY_BY_HEADER = "by_headers";
        private List<String> byHeaders = null;

        public static final String JSON_PROPERTY_BY_PAYLOAD = "by_payload";
        private List<String> byPayload = null;

        public OsisS3CapabilitiesExclusions all(boolean all) {

            this.all = all;
            return this;
        }

        /**
         * Get all
         *
         * @return all
         **/
        @ApiModelProperty(value = "")
        @JsonProperty(JSON_PROPERTY_ALL)
        @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)

        public boolean getAll() {
            return all;
        }


        public void setAll(boolean all) {
            this.all = all;
        }


        public OsisS3CapabilitiesExclusions byParams(List<String> byParams) {

            this.byParams = byParams;
            return this;
        }

        public OsisS3CapabilitiesExclusions addByParamsItem(String byParamsItem) {
            if (this.byParams == null) {
                this.byParams = new ArrayList<>();
            }
            this.byParams.add(byParamsItem);
            return this;
        }

        /**
         * Get byParams
         *
         * @return byParams
         **/
        @ApiModelProperty(value = "")
        @JsonProperty(JSON_PROPERTY_BY_PARAMS)
        @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)

        public List<String> getByParams() {
            return byParams;
        }


        public void setByParams(List<String> byParams) {
            this.byParams = byParams;
        }


        public OsisS3CapabilitiesExclusions byHeader(List<String> byHeader) {

            this.byHeaders = byHeader;
            return this;
        }

        public OsisS3CapabilitiesExclusions addByHeaderItem(String byHeaderItem) {
            if (this.byHeaders == null) {
                this.byHeaders = new ArrayList<>();
            }
            this.byHeaders.add(byHeaderItem);
            return this;
        }

        /**
         * Get byHeader
         *
         * @return byHeader
         **/
        @ApiModelProperty(value = "")
        @JsonProperty(JSON_PROPERTY_BY_HEADER)
        @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)
        public List<String> getByHeaders() {
            return byHeaders;
        }


        public void setByHeaders(List<String> byHeaders) {
            this.byHeaders = byHeaders;
        }


        public OsisS3CapabilitiesExclusions byPayload(List<String> byPayload) {

            this.byPayload = byPayload;
            return this;
        }

        public OsisS3CapabilitiesExclusions addByPayloadItem(String byPayloadItem) {
            if (this.byPayload == null) {
                this.byPayload = new ArrayList<>();
            }
            this.byPayload.add(byPayloadItem);
            return this;
        }

        /**
         * Get byPayload
         *
         * @return byPayload
         **/
        @ApiModelProperty(value = "")
        @JsonProperty(JSON_PROPERTY_BY_PAYLOAD)
        @JsonInclude(value = JsonInclude.Include.USE_DEFAULTS)

        public List<String> getByPayload() {
            return byPayload;
        }


        public void setByPayload(List<String> byPayload) {
            this.byPayload = byPayload;
        }


        @Override
        public boolean equals(java.lang.Object o) {
            if (this == o) {
                return true;
            }
            if (o == null || getClass() != o.getClass()) {
                return false;
            }
            OsisS3CapabilitiesExclusions osisS3CapabilitiesExclusions = (OsisS3CapabilitiesExclusions) o;
            return Objects.equals(this.all, osisS3CapabilitiesExclusions.all) &&
                    Objects.equals(this.byParams, osisS3CapabilitiesExclusions.byParams) &&
                    Objects.equals(this.byHeaders, osisS3CapabilitiesExclusions.byHeaders) &&
                    Objects.equals(this.byPayload, osisS3CapabilitiesExclusions.byPayload);
        }

        @Override
        public int hashCode() {
            return Objects.hash(all, byParams, byHeaders, byPayload);
        }


        @Override
        public String toString() {
            StringBuilder sb = new StringBuilder();
            sb.append("class OsisS3CapabilitiesExclusions {\n");
            sb.append("    all: ").append(toIndentedString(all)).append("\n");
            sb.append("    byParams: ").append(toIndentedString(byParams)).append("\n");
            sb.append("    byHeader: ").append(toIndentedString(byHeaders)).append("\n");
            sb.append("    byPayload: ").append(toIndentedString(byPayload)).append("\n");
            sb.append("}");
            return sb.toString();
        }

        /**
         * Convert the given object to string with each line indented by 4 spaces
         * (except the first line).
         */
        private String toIndentedString(java.lang.Object o) {
            if (o == null) {
                return "null";
            }
            return o.toString().replace("\n", "\n    ");
        }

    }
}

