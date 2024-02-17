/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Sample6Root } from '../models/Sample6Root';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class Sample6Service {
    /**
     * Get Page Info
     * @returns Sample6Root Successful Response
     * @throws ApiError
     */
    public static getPageInfo(): CancelablePromise<Sample6Root> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sample_6/page-info',
        });
    }
}
