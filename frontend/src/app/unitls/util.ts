import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';

export type Framework = 'CSRD' | 'SASB' | 'GRI' | 'CDP';
export type Tone = 'regulatory' | 'investor_friendly';

export interface Metric {
  name: string;
  value: string;
  unit?: string;
}

export interface GenerateDisclosureRequest {
  company_name: string;
  sector: string;
  year: number;
  frameworks: Framework[];
  metrics: Metric[];
  initiatives: string;
  tone: Tone;
}

export interface GenerateDisclosureResponse {
  disclosure_text: string;
  improvement_suggestions: string[];
  model?: string;
  prompt_tokens?: number;
  completion_tokens?: number;
  total_tokens?: number;
}

export interface HistoryItem {
  id: number;
  company_name: string;
  year: number;
  frameworks: Framework[];
  created_at: string;
  disclosure_preview: string;
}
