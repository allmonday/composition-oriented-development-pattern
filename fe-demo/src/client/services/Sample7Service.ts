/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Sample7TaskDetail } from '../models/Sample7TaskDetail';
import type { Sample7TeamDetail } from '../models/Sample7TeamDetail';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class Sample7Service {
    /**
     * Get Tasks
     * @returns Sample7TaskDetail Successful Response
     * @throws ApiError
     */
    public static getTasks(): CancelablePromise<Array<Sample7TaskDetail>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sample_7/tasks',
        });
    }
    /**
     * Get User Stat
     * @returns Sample7TeamDetail Successful Response
     * @throws ApiError
     */
    public static getUserStat(): CancelablePromise<Array<Sample7TeamDetail>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sample_7/user/stat',
        });
    }
}
