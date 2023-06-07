import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, of, throwError } from 'rxjs';
import { SocialAuthService } from "@abacritt/angularx-social-login";
import jwt_decode from "jwt-decode";

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private _isLoggedIn$ = new BehaviorSubject<boolean>(false);
  isLoggedIn$ = this._isLoggedIn$.asObservable();

  // baseURL: string = "https://57mejk64tc.execute-api.us-east-1.amazonaws.com"
  baseURL: string = "http://localhost:5000"

  constructor (
    private http: HttpClient, 
    private socialAuthService: SocialAuthService
  ) {
      const token = localStorage.getItem('token') 
      this._isLoggedIn$.next(!!token);
    }

  login(token: string): void { 
    localStorage.setItem('token', JSON.stringify(token));
    this._isLoggedIn$.next(!!token);
    this.http.get<any>(`${this.baseURL}/lesson`).subscribe((data) => console.log(data))
  }

  logout(): void {
    localStorage.removeItem('token');
    this._isLoggedIn$.next(false);
  }

  // Ideally I should do this server side
  decodeToken(token: string): any {
    // console.log('data')
    // console.log(jwt_decode(token))
    return jwt_decode(token);
  }
}
