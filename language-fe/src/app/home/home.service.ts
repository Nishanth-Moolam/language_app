import { Injectable } from "@angular/core";
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, of, throwError } from 'rxjs';
import { AuthService } from '../auth.service';
import { Lesson } from './models/lesson.interface';

@Injectable({
  providedIn: 'root',
})
export class HomeService {
  baseURL: string;

  private _lessonList = new BehaviorSubject<Lesson[]>([]);
  private _tabIndex = new BehaviorSubject<number>(0);
  lessonList = this._lessonList.asObservable();
  tabIndex = this._tabIndex.asObservable();

  constructor(private http: HttpClient, private authService: AuthService) {
    this.baseURL = this.authService.baseURL;
  }

  setLessonList(lessonList: Lesson[]): Observable<Lesson[]> {
    this._lessonList.next(lessonList);
    return this.lessonList;
  }

  setTabIndex(tabIndex: number): Observable<number> {
    this._tabIndex.next(tabIndex);
    return this.tabIndex;
  }

  postLesson(lesson: Lesson): Observable<any> {
    return this.http.post<any>(`${this.baseURL}/lesson`, lesson);
  }

  getLessonList(): Observable<any> {
    return this.http.get<any>(`${this.baseURL}/lesson`);
  }

  getLesson(id: any): Observable<any> {
    return this.http.get<any>(`${this.baseURL}/lesson/${id}`);
  }

  deleteLesson(id: any): Observable<any> {
    return this.http.delete<any>(`${this.baseURL}/lesson/${id}`);
  }

  changeKnowledge(id: any, knowledge: number): Observable<any> {
    return this.http.put<any>(`${this.baseURL}/word/knowledge/${id}`, {
      knowledge,
    });
  }

  addTranslation(id: any, translation: string): Observable<any> {
    return this.http.post<any>(`${this.baseURL}/word/translation/${id}`, {
      translation,
    });
  }

  deleteTranslation(id: any, translation: string): Observable<any> {
    return this.http.put<any>(`${this.baseURL}/word/translation/${id}`, {
      translation,
    });
  }
}