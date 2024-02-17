/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Sample1SprintDetail } from './Sample1SprintDetail';
import type { User } from './User';
export type Sample1TeamDetail = {
    id: number;
    name: string;
    sprints?: Array<Sample1SprintDetail>;
    members?: Array<User>;
};

