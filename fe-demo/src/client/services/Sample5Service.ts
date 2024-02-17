/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Sample5Root } from '../models/Sample5Root';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class Sample5Service {
    /**
     * Get Page Info
     * @param teamId
     * @returns Sample5Root Successful Response
     * @throws ApiError
     */
    public static getPageInfo(
        teamId: number,
    ): CancelablePromise<Sample5Root> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sample_5/page-info/{team_id}',
            path: {
                'team_id': teamId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
