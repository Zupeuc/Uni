def choque_malos(self, entity):
    print('Hitbox Malo:')
    print(self.hitbox)
    print('Hitbox Heroe:')
    print(entity)
    # Choque desde abajo
    if (self.hitbox[0] <= entity[2]) and (self.hitbox[0] >= entity[0]) and \
            (self.hitbox[1] >= entity[3]) and self.hitbox[3] >= entity[1]:
        return True
    if (self.hitbox[2] <= entity[2]) and (self.hitbox[2] >= entity[0]) and \
            (self.hitbox[1] >= entity[3]) and (self.hitbox[3] >= entity[1]):
        return True
    # Choque desde arriba
    if (self.hitbox[0] <= entity[2]) and (self.hitbox[0] >= entity[0]) and \
            (self.hitbox[1] >= entity[1]) and (self.hitbox[3] <= entity[1]):
        return True
    if (self.hitbox[2] <= entity[2]) and (self.hitbox[2] >= entity[0]) and \
            (self.hitbox[1] >= entity[1]) and (self.hitbox[3] <= entity[1]):
        return True
    # Choque desde la derecha
    if (self.hitbox[1] >= entity[3]) and (self.hitbox[1] <= entity[3]) and \
            (self.hitbox[2] >= entity[0]) and (self.hitbox[0] <= entity[0]):
        return True
    if (self.hitbox[3] >= entity[3]) and (self.hitbox[3] <= entity[1]) and \
            (self.hitbox[2] >= entity[0]) and (self.hitbox[0] <= entity[0]):
        return True
    # Choque desde la izquierda
    if (self.hitbox[1] >= entity[3]) and (self.hitbox[1] <= entity[3]) and \
            (self.hitbox[0] <= entity[2]) and (self.hitbox[2] >= entity[2]):
        return True
    if (self.hitbox[3] >= entity[3]) and (self.hitbox[3] <= entity[1]) and \
            (self.hitbox[0] <= entity[2]) and (self.hitbox[2] >= entity[2]):
        return True
    else:
        print('sugoi')
        return False


def choque_malos_old(self, entity):
    # Choque desde abajo
    print('2')
    print(entity)
    if (self.hitbox[0] <= entity[2]) and (self.hitbox[0] >= entity[0]) and self.hitbox[1] == entity[3]:
        return True
    elif (self.hitbox[2] <= entity[2]) and (self.hitbox[2] >= entity[0]) and self.hitbox[1] == entity[3]:
        return True
    # Choque desde arriba
    elif (self.hitbox[0] <= entity[2]) and (self.hitbox[0] >= entity[0]) and self.hitbox[3] == entity[1]:
        return True
    elif (self.hitbox[2] <= entity[2]) and (self.hitbox[2] >= entity[0]) and self.hitbox[3] == entity[1]:
        return True
    # Choque desde la derecha
    elif (self.hitbox[1] >= entity[3]) and (self.hitbox[1] <= entity[3]) and self.hitbox[2] == entity[0]:
        return True
    elif (self.hitbox[3] >= entity[3]) and (self.hitbox[3] <= entity[1]) and self.hitbox[2] == entity[0]:
        return True
    # Choque desde la izquierda
    elif (self.hitbox[1] >= entity[3]) and (self.hitbox[1] <= entity[3]) and self.hitbox[0] == entity[2]:
        return True
    elif (self.hitbox[3] >= entity[3]) and (self.hitbox[3] <= entity[1]) and self.hitbox[0] == entity[2]:
        return True
    else:
        print('sugoi')
        return False


def choque_malos_old2(self, entity):
            # Choque desde abajo
            if (self.hitbox[0] <= entity.hitbox[2]) and (self.hitbox[0] >= entity.hitbox[0]) and \
                            self.hitbox[1] == entity.hitbox[3]:
                return True
            elif (self.hitbox[2] <= entity.hitbox[2]) and (self.hitbox[2] >= entity.hitbox[0]) and \
                            self.hitbox[1] == entity.hitbox[3]:
                return True
            # Choque desde arriba
            elif (self.hitbox[0] <= entity.hitbox[2]) and (self.hitbox[0] >= entity.hitbox[0]) and \
                            self.hitbox[3] == entity.hitbox[1]:
                return True
            elif (self.hitbox[2] <= entity.hitbox[2]) and (self.hitbox[2] >= entity.hitbox[0]) and \
                            self.hitbox[3] == entity.hitbox[1]:
                return True
            # Choque desde la derecha
            elif (self.hitbox[1] >= entity.hitbox[3]) and (self.hitbox[1] <= entity.hitbox[3]) and \
                            self.hitbox[2] == entity.hitbox[0]:
                return True
            elif (self.hitbox[3] >= entity.hitbox[3]) and (self.hitbox[3] <= entity.hitbox[1]) and \
                            self.hitbox[2] == entity.hitbox[0]:
                return True
            # Choque desde la izquierda
            elif (self.hitbox[1] >= entity.hitbox[3]) and (self.hitbox[1] <= entity.hitbox[3]) and \
                            self.hitbox[0] == entity.hitbox[2]:
                return True
            elif (self.hitbox[3] >= entity.hitbox[3]) and (self.hitbox[3] <= entity.hitbox[1]) and \
                            self.hitbox[0] == entity.hitbox[2]:
                return True
            else:
                return False



