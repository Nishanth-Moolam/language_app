import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, of, throwError } from 'rxjs';
import {
  GoogleLoginProvider,
  SocialAuthService,
} from '@abacritt/angularx-social-login';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private _isLoggedIn$ = new BehaviorSubject<boolean>(false);
  isLoggedIn$ = this._isLoggedIn$.asObservable();
  user: Observable<any> = of({});

  get token() {
    return localStorage.getItem('token');
  }

  baseURL: string = 'https://57mejk64tc.execute-api.us-east-1.amazonaws.com';
  // baseURL: string = 'http://localhost:5000';

  constructor(
    private http: HttpClient,
    private socialAuthService: SocialAuthService
  ) {
    this._isLoggedIn$.next(!!this.token);
    if (this.token) {
      this.user = this.http.get<any>(`${this.baseURL}/login`);
    }
  }

  login(token: string): Observable<any> {
    localStorage.setItem('token', JSON.stringify(token));
    this._isLoggedIn$.next(!!token);

    this.user = this.http.get<any>(`${this.baseURL}/login`);

    return this.user;
  }

  logout(): void {
    localStorage.removeItem('token');
    this._isLoggedIn$.next(false);
    this.socialAuthService.signOut();
    this.user = of({});
  }

  // not sure when to use this
  refreshToken(): void {
    this.socialAuthService.refreshAuthToken(GoogleLoginProvider.PROVIDER_ID);
  }
}
