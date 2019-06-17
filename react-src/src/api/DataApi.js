import {GET} from './apiRequest';

class UserApi {
    static getMoisture() {
        return GET('moisture');
    }

    static getLastWatered() {
        return GET('water')
    }
}

export default UserApi;