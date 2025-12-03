import { Component, signal, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormArray,
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
} from '@angular/forms';
import {
  EsgAiService,
} from './services/esg-ai.service';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatRadioModule } from '@angular/material/radio';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import {Framework, GenerateDisclosureResponse, HistoryItem} from './unitls/util';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatCheckboxModule,
    MatRadioModule,
    MatButtonModule,
    MatProgressSpinnerModule,],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  // Angular 17 DI with inject()
  private readonly fb = inject(FormBuilder);
  private readonly esgAiService = inject(EsgAiService);

  // Signals for UI state
  readonly loading = signal(false);
  readonly errorMessage = signal<string | null>(null);
  readonly result = signal<GenerateDisclosureResponse | null>(null);
  readonly historyItems = signal<HistoryItem[]>([]);

  readonly frameworksList: Framework[] = ['CSRD', 'SASB', 'GRI', 'CDP'];

  // Reactive form
  readonly form: FormGroup = this.fb.group({
    company_name: ['Acme Corp'],
    sector: ['Technology'],
    year: [2024],
    tone: ['regulatory'],
    initiatives: [
      'We migrated data centers to renewable electricity and launched an inclusion program.',
    ],
    frameworks: this.fb.group({
      CSRD: [true],
      SASB: [false],
      GRI: [false],
      CDP: [false],
    }),
    metrics: this.fb.array([
      this.createMetric('Scope 1 emissions', '12000', 'tCO2e'),
      this.createMetric('% women on board', '42', '%'),
    ]),
  });

  constructor() {
    this.refreshHistory();
  }

  // ---- metrics helpers ----
  get metrics(): FormArray {
    return this.form.get('metrics') as FormArray;
  }

  createMetric(name = '', value = '', unit = ''): FormGroup {
    return this.fb.group({
      name: [name],
      value: [value],
      unit: [unit],
    });
  }

  addMetric(): void {
    this.metrics.push(this.createMetric());
  }

  removeMetric(index: number): void {
    this.metrics.removeAt(index);
  }

  // ---- API helpers ----
  private refreshHistory(): void {
    this.esgAiService.getHistory().subscribe({
      next: (items) => this.historyItems.set(items),
      error: () => {
        // ignore errors for demo
      },
    });
  }

  submit(): void {
    this.errorMessage.set(null);
    this.result.set(null);

    if (this.form.invalid) {
      this.errorMessage.set('Please fill all required fields.');
      return;
    }

    const raw = this.form.value;

    const frameworksGroup = raw.frameworks as Record<string, boolean>;
    const frameworks = Object.entries(frameworksGroup)
      .filter(([_, checked]) => checked)
      .map(([name]) => name as Framework);

    const payload = {
      company_name: raw.company_name!,
      sector: raw.sector!,
      year: raw.year!,
      tone: raw.tone!,
      initiatives: raw.initiatives!,
      frameworks,
      metrics: (raw.metrics ?? []).map((m: any) => ({
        name: m.name,
        value: m.value,
        unit: m.unit,
      })),
    };

    this.loading.set(true);

    this.esgAiService.generateDisclosure(payload).subscribe({
      next: (res) => {
        this.result.set(res);
        this.loading.set(false);
        this.refreshHistory();
      },
      error: () => {
        this.errorMessage.set('Something went wrong while generating.');
        this.loading.set(false);
      },
    });
  }
}
