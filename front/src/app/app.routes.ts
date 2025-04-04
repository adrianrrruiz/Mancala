import { Routes } from '@angular/router';
import { StartComponent } from './components/start/start.component';
import { GameComponent } from './components/game/game.component';
import { PlayerFormComponent } from './components/player-form/player-form.component';


export const routes: Routes = [
    { path: '', component: StartComponent },
    { path: 'vs-player', component: PlayerFormComponent, data: { mode: 'vs-player' } },
    { path: 'vs-machine', component: PlayerFormComponent, data: { mode: 'vs-machine' } },
    { path: 'machine-vs-machine', component: PlayerFormComponent, data: { mode: 'machine-vs-machine' } },
    { path: 'game', component: GameComponent },
    { path: '**', redirectTo: '' }, // Redirección si la ruta no existe
];
