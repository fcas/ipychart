// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

import { test } from '@jupyterlab/galata';

import { expect } from '@playwright/test';

import * as path from 'path';

async function sleep(time: number) {
    return await new Promise((resolve) => setTimeout(resolve, time));
}

test.describe('Widget Visual Regression', () => {
    let captures: Buffer[] = [];
    let cellCount: number | undefined;
    const notebook = 'ipychart-test-notebook.ipynb';

    test.beforeEach(async ({ page, tmpPath }) => {
        await page.contents.uploadDirectory(path.resolve(__dirname, './notebooks'), tmpPath);
        await page.filebrowser.openDirectory(tmpPath);
    });

    test('Run notebook ipychart-test-notebook.ipynb and capture cell outputs', async ({ page, tmpPath }) => {
        await page.notebook.openByPath(`${tmpPath}/${notebook}`);
        await page.notebook.activate(notebook);
        await page.waitForTimeout(500);

        cellCount = await page.notebook.getCellCount();

        captures = new Array<Buffer>();

        await page.notebook.runCellByCell({
            onAfterCellRun: async (cellIndex: number) => {
                const cell = await page.notebook.getCellOutputLocator(cellIndex);
                if (cell) {
                    await sleep(1000);
                    captures.push(await cell.screenshot({ animations: 'disabled' }));
                }
            },
        });

        await page.notebook.save();
    });

    // Adjust the maximum number of cells as needed
    for (let i = 0; i < 25; i++) {
        test(`Compare output of cell ${i}`, async () => {
            if (typeof cellCount === 'undefined' || i >= cellCount) {
                test.skip();
            } else {
                const image = `${notebook}-cell-${i}.png`;
                expect
                    .soft(captures[i])
                    .toMatchSnapshot(image, { threshold: 0.5, maxDiffPixelRatio: 0.03 });
            }
        });
    }
});