/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Sample1SprintDetail } from '../models/Sample1SprintDetail';
import type { Sample1StoryDetail } from '../models/Sample1StoryDetail';
import type { Sample1TaskDetail } from '../models/Sample1TaskDetail';
import type { Sample1TeamDetail } from '../models/Sample1TeamDetail';
import type { Sample1TeamDetail2 } from '../models/Sample1TeamDetail2';
import type { Task } from '../models/Task';
import type { User } from '../models/User';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class Sample1Service {
    /**
     * Get Users
     * 1.1 return list of user
     * @returns User Successful Response
     * @throws ApiError
     */
    public static getUsers(): CancelablePromise<Array<User>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sample_1/users',
        });
    }
    /**
     * Get Tasks
     * 1.2 return list of tasks
     * @returns Task Successful Response
     * @throws ApiError
     */
    public static getTasks(): CancelablePromise<Array<Task>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sample_1/tasks',
        });
    }
    /**
     * Get Tasks With Detail
     * 1.3 return list of tasks(user)
     * @returns Sample1TaskDetail Successful Response
     * @throws ApiError
     */
    public static getTasksWithDetail(): CancelablePromise<Array<Sample1TaskDetail>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sample_1/tasks-with-detail',
        });
    }
    /**
     * Get Stories With Detail
     * 1.4 return list of story(task(user))
     * @returns Sample1StoryDetail Successful Response
     * @throws ApiError
     */
    public static getStoriesWithDetail(): CancelablePromise<Array<Sample1StoryDetail>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sample_1/stories-with-detail',
        });
    }
    /**
     * Get Sprints With Detail
     * 1.5 return list of sprint(story(task(user)))
     * @returns Sample1SprintDetail Successful Response
     * @throws ApiError
     */
    public static getSprintsWithDetail(): CancelablePromise<Array<Sample1SprintDetail>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sample_1/sprints-with-detail',
        });
    }
    /**
     * Get Teams With Detail
     * 1.6 return list of team(sprint(story(task(user))))
     * @returns Sample1TeamDetail Successful Response
     * @throws ApiError
     */
    public static getTeamsWithDetail(): CancelablePromise<Array<Sample1TeamDetail>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sample_1/teams-with-detail',
        });
    }
    /**
     * Get Teams With Detail 2
     * 1.7 return list of team(sprint(story(task(user))))
     * @returns Sample1TeamDetail2 Successful Response
     * @throws ApiError
     */
    public static getTeamsWithDetail2(): CancelablePromise<Array<Sample1TeamDetail2>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/sample_1/teams-with-detail2',
        });
    }
}
