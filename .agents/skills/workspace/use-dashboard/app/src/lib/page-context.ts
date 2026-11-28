import { type Context, createContext } from 'react';

export interface OpenPage {
  dashboardTitle: string;
  pageTitle: string;
}

export const OpenPageContext: Context<OpenPage> = createContext<OpenPage>({ dashboardTitle: '', pageTitle: '' });
