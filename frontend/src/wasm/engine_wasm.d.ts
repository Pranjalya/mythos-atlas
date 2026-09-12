/* tslint:disable */
/* eslint-disable */

export class TimelineEngine {
    free(): void;
    [Symbol.dispose](): void;
    /**
     * Loads JSON array of MythRecord items and builds the interval tree.
     */
    load_records(records_json: string): boolean;
    constructor();
    /**
     * Queries active myths for a given year, returning an array of ActiveMythResult objects.
     */
    query_timeline(year: number): any;
    /**
     * Returns the total count of loaded records.
     */
    total_records(): number;
}

/**
 * Global WASM function: loads records into the global timeline engine.
 */
export function load_records(records_json: string): boolean;

/**
 * Global WASM function: queries active myths from the global timeline engine.
 */
export function query_timeline(year: number): any;

export type InitInput = RequestInfo | URL | Response | BufferSource | WebAssembly.Module;

export interface InitOutput {
    readonly memory: WebAssembly.Memory;
    readonly __wbg_timelineengine_free: (a: number, b: number) => void;
    readonly load_records: (a: number, b: number) => number;
    readonly query_timeline: (a: number) => any;
    readonly timelineengine_load_records: (a: number, b: number, c: number) => number;
    readonly timelineengine_new: () => number;
    readonly timelineengine_query_timeline: (a: number, b: number) => any;
    readonly timelineengine_total_records: (a: number) => number;
    readonly __wbindgen_externrefs: WebAssembly.Table;
    readonly __wbindgen_malloc: (a: number, b: number) => number;
    readonly __wbindgen_realloc: (a: number, b: number, c: number, d: number) => number;
    readonly __wbindgen_start: () => void;
}

export type SyncInitInput = BufferSource | WebAssembly.Module;

/**
 * Instantiates the given `module`, which can either be bytes or
 * a precompiled `WebAssembly.Module`.
 *
 * @param {{ module: SyncInitInput }} module - Passing `SyncInitInput` directly is deprecated.
 *
 * @returns {InitOutput}
 */
export function initSync(module: { module: SyncInitInput } | SyncInitInput): InitOutput;

/**
 * If `module_or_path` is {RequestInfo} or {URL}, makes a request and
 * for everything else, calls `WebAssembly.instantiate` directly.
 *
 * @param {{ module_or_path: InitInput | Promise<InitInput> }} module_or_path - Passing `InitInput` directly is deprecated.
 *
 * @returns {Promise<InitOutput>}
 */
export default function __wbg_init (module_or_path?: { module_or_path: InitInput | Promise<InitInput> } | InitInput | Promise<InitInput>): Promise<InitOutput>;
