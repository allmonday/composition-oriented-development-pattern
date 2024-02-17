/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Sample2TeamDetail } from '../models/Sample2TeamDetail';
import type { Sample2TeamDetailMultipleLevel } from '../models/Sample2TeamDetailMultipleLevel';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class Sample2Service {
    /**
     * Get Teams With Detail
     * 1.1 teams with senior members
     * @returns Sample2TeamDetail Successful Response
     * @throws ApiError
     */
    public static getTeamsWithDetail(): CancelablePromise<Array<Sample2TeamDetail>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sample_2/teams-with-detail',
        });
    }
    /**
     * Get Teams With Detail Of Multiple Level
     * 1.2 teams with senior and junior members
     * @returns Sample2TeamDetailMultipleLevel Successful Response
     * @throws ApiError
     */
    public static getTeamsWithDetailOfMultipleLevel(): CancelablePromise<Array<Sample2TeamDetailMultipleLevel>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sample_2/teams-with-detail-of-multiple-level',
        });
    }
}
