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
  }

  logout(): void {
    //delete token from local storage
  }

  // Ideally I should do this server side
  decodeToken(token: string): any {
    return jwt_decode(token);
  }
}
