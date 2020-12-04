class Guest:
    def __init__(self, id: int, key: int, cabinets: set):
        self.name = "Посетитель"
        self.id = id
        self.key = key
        self.cabinets = cabinets
        self.tg_id = -1

    def remove_cabinet(self, cabinet_id):
        for c in self.cabinets:
            if c == cabinet_id:
                self.cabinets.remove(c)
                break

    def set_name(self, name: str):
        self.name = name

    def __str__(self):
        cabs = list()
        for cab in self.cabinets:
            cabs.append(str(cab))
        return f'Name: {self.name}, ID: {self.id}, tg_id: {self.tg_id}, cabinet_ids: {", ".join(cabs)}'


class Worker:
    def __init__(self, key: int, cab_id: int, name="Default_name", ):
        self.tg_id = -1
        self.key = key
        self.name = name
        self.cab_id = cab_id

    def set_name(self, name: str):
        self.name = name

    def __str__(self):
        return f'Name: {self.name}, tg_id: {self.tg_id}, cab_id: {self.cab_id}'


class Cabinet:
    # Time in seconds
    def __init__(self, id: int, name: str, average_time: int):
        self.query = list()
        self.name = name
        self.average_time = average_time
        self.id = id
        self.worker = Worker(0, id)
        self.current_guest_id = 0

    def count_time(self, guest: Guest):
        for i in range(0, len(self.query)):
            if self.query[i].id > guest.id:
                return i * self.average_time
        return len(self.query) * self.average_time

    def added_count_time(self, guest: Guest):
        for i in range(0, len(self.query)):
            if self.query[i].id == guest.id:
                return i * self.average_time

    def add_guest(self, guest: Guest):
        added = False
        for i in range(0, len(self.query)):
            if self.query[i].id > guest.id:
                self.query.insert(i, guest)
                added = True
                break
        if not added:
            self.query.append(guest)

    def next_guest(self, ids: dict):
        ids['prev'] = self.query[0]
        self.query.pop(0)
        ids['next'] = self.query[0]

    def change_worker(self, worker: Worker):
        self.worker = worker

    def __str__(self):
        if len(self.query) == 0:
            answer = f'Name: {self.name}, ID: {self.id}, time: {self.average_time}, query:\n' \
                     f'Worker: {str(self.worker)}'
        else:
            que = list()
            for q in self.query:
                que.append(str(q))
            ques = str("\n".join(que))
            answer = f'Name: {self.name}, ID: {self.id}, time: {self.average_time}, query:\n' \
                     f'Посетители, для которых этот кабинет следующий: кабинет: {ques}\n' \
                     f'Worker: {str(self.worker)}'
        return answer


class Schedule:
    def __init__(self):
        self.admins_id = {321354512, 914239664}
        self.cabinets = dict()
        self.authorized_guests = dict()
        self.authorized_workers = dict()
        self.guests = dict()
        self.workers = dict()
        self.id_for_guest = 0
        self.id_for_worker = 0
        self.id_for_cabinet = 0

    def get_permission(self, tg_id: int):
        """
        1 - admin
        2 - worker
        3 - guest
        0 - not registered
        :param tg_id:
        :return:
        """
        if tg_id in self.admins_id:
            return 1
        elif tg_id in self.authorized_workers.keys():
            return 2
        elif tg_id in self.authorized_guests.keys():
            return 3
        else:
            return 0

    def id_guest(self):
        self.id_for_guest += 1
        return self.id_for_guest - 1

    def id_worker(self):
        self.id_for_worker += 1
        return self.id_for_worker - 1

    def id_cabinet(self):
        self.id_for_cabinet += 1
        return self.id_for_cabinet - 1

    def add_guest(self, guest: Guest):
        self.guests[guest.id] = guest
        min_id = -1
        min_time = 10000000
        for cab in guest.cabinets:
            cab = self.cabinets[cab]
            if cab.count_time(guest) < min_time:
                min_id = cab.id
                min_time = cab.count_time(guest)
        if min_id != -1:
            self.cabinets[min_id].add_guest(guest)

    def add_cabinet(self, cabinet: Cabinet):
        self.cabinets[cabinet.id] = cabinet

    def add_worker(self, worker: Worker):
        self.workers[worker.cab_id] = worker
        self.cabinets[worker.cab_id].worker = worker

    def set_guest_id(self, key: int, tg_id: int) -> bool:
        for g in self.guests.keys():
            if self.guests[g].key == key:
                self.guests[g].tg_id = tg_id
                self.authorized_guests[tg_id] = self.guests[g]
                return True
        return False

    def set_worker_id(self, key: int, tg_id: int) -> bool:
        for w in self.workers.keys():
            if self.workers[w].key == key:
                self.workers[w].tg_id = tg_id
                self.authorized_workers[tg_id] = self.workers[w]
                return True
        return False

    def next_guest(self, tg_id: int, ids: dict):
        cab_id = self.authorized_workers[tg_id].cab_id
        ids = dict()
        self.cabinets[cab_id].next_guest(ids)
        guest = 1
        for g in self.guests.keys():
            if self.guests[g].id == ids['prev'].id:
                if self.guests[g].tg_id != -1:
                    self.authorized_guests[g.tg_id].remove_cabinet(cab_id)
                self.guests[g].remove_cabinet(cab_id)
                guest = self.guests[g]
                break
        min_id = -1
        min_time = 10000000
        for cab in guest.cabinets:
            if self.cabinets[cab].count_time(guest) < min_time:
                min_id = cab
                min_time = self.cabinets[cab].count_time(guest)
        if min_id != -1:
            self.cabinets[min_id].add_guest(guest)

    def count_time_guest(self, tg_id: int):
        for cab in self.cabinets.keys():
            if self.authorized_guests[tg_id] in self.cabinets[cab].query:
                return self.cabinets[cab].added_count_time(self.authorized_guests[tg_id])
        return "Empty"

    def change_worker_name(self, tg_id: int, name: str):
        self.authorized_workers[tg_id].name = name
        for id in range(0, len(self.workers)):
            if self.workers[id].tg_id == tg_id:
                self.workers[id].name = name

    def get_tg_guest(self, id):
        return self.guests[id].tg_id

    def __str__(self):
        cabs = list()
        for c in self.cabinets.keys():
            cabs.append(f"{str(self.cabinets[c])}")
        answer = 'cabinets:\n'
        answer += '\n\n'.join(cabs)
        return answer
