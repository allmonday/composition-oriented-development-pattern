/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Sample3TeamDetail } from '../models/Sample3TeamDetail';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class Sample3Service {
    /**
     * Get Teams With Detail
     * 1.1 expose (provide) ancestor data to descendant node.
     * @returns Sample3TeamDetail Successful Response
     * @throws ApiError
     */
    public static getTeamsWithDetail(): CancelablePromise<Array<Sample3TeamDetail>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sample_3/teams-with-detail',
        });
    }
}
