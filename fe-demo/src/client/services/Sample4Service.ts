/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Sample4TeamDetail } from '../models/Sample4TeamDetail';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class Sample4Service {
    /**
     * Get Teams With Detail
     * @returns Sample4TeamDetail Successful Response
     * @throws ApiError
     */
    public static getTeamsWithDetail(): CancelablePromise<Array<Sample4TeamDetail>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sample_4/teams-with-detail',
        });
    }
}
