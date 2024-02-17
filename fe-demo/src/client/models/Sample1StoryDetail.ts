/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Sample1TaskDetail } from './Sample1TaskDetail';
import type { User } from './User';
export type Sample1StoryDetail = {
    id: number;
    name: string;
    owner_id: number;
    sprint_id: number;
    tasks?: Array<Sample1TaskDetail>;
    owner?: (User | null);
};

