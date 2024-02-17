/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Sample4TaskDetail } from './Sample4TaskDetail';
export type Sample4StoryDetail = {
    id: number;
    name: string;
    owner_id: number;
    sprint_id: number;
    tasks?: Array<Sample4TaskDetail>;
    task_count?: number;
};

