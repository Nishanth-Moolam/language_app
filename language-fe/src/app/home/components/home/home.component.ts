import { GoogleLoginProvider, SocialAuthService } from '@abacritt/angularx-social-login';
import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { HomeService } from '../../home.service';
import { AuthService } from 'src/app/auth.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class HomeComponent implements OnInit {

  fullName: string = '';
  isLoggedIn: boolean = false;

  constructor(private socialAuthService: SocialAuthService, private authService: AuthService) { }

  ngOnInit(): void {
    this.socialAuthService.authState.subscribe((user) => {
      this.authService.login(user.idToken);
    });

    this.authService.isLoggedIn$.subscribe((isLoggedIn) => {
      this.isLoggedIn = isLoggedIn;
      if (isLoggedIn) {
        const token = localStorage.getItem('token') || ''
        this.fullName = this.authService.decodeToken(token)?.name || '';
      }
    })
  }

  // not sure when to use this
  refreshToken(): void {
    this.socialAuthService.refreshAuthToken(GoogleLoginProvider.PROVIDER_ID);
  }
}
