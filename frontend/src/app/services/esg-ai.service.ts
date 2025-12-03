import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import {GenerateDisclosureRequest, GenerateDisclosureResponse, HistoryItem} from '../unitls/util';


@Injectable({ providedIn: 'root' })
export class EsgAiService {
  private readonly baseUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) {}

  generateDisclosure(
    body: GenerateDisclosureRequest
  ): Observable<GenerateDisclosureResponse> {
    return this.http.post<GenerateDisclosureResponse>(
      `${this.baseUrl}/api/generate-disclosure`,
      body
    );
  }

  getHistory(limit = 10): Observable<HistoryItem[]> {
    return this.http.get<HistoryItem[]>(`${this.baseUrl}/api/history`, {
      params: { limit } as any,
    });
  }
}
