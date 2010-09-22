#===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import eos.db
import eos.types
import copy

class Character():
    instance = None
    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Character()

        return cls.instance

    def all0ID(self):
        all0 = eos.types.Character.getAll0()
        eos.db.commit()
        return all0.ID

    def getCharacterList(self):
        baseChars = [eos.types.Character.getAll0(), eos.types.Character.getAll5()]
        # Flush incase all0 & all5 weren't in the db yet
        eos.db.commit()
        return map(lambda c: (c.ID, c.name), eos.db.getCharacterList())

    def getSkillGroups(self):
        marketGroup = eos.db.getMarketGroup(150)
        return map(lambda mg: (mg.ID, mg.name), marketGroup.children)

    def getSkills(self, groupID):
        marketGroup = eos.db.getMarketGroup(groupID)
        skills = []
        for skill in marketGroup.items:
            skills.append((skill.ID, skill.name))
        return skills

    def getSkillDescription(self, itemID):
        return eos.db.getItem(itemID).description

    def getGroupDescription(self, groupID):
        return eos.db.getMarketGroup(groupID).description

    def getSkillLevel(self, charID, skillID):
        skill = eos.db.getCharacter(charID).getSkill(skillID)
        return skill.level if skill.learned else "Not learned"

    def rename(self, charID, newName):
        char = eos.db.getCharacter(charID)
        char.name = newName
        eos.db.commit()

    def new(self):
        char = eos.types.Character("New Character")
        eos.db.save(char)
        return char.ID

    def getCharName(self, charID):
        return eos.db.getCharacter(charID).name

    def copy(self, charID):
        char = eos.db.getCharacter(charID)
        newChar = copy.deepcopy(char)
        eos.db.save(newChar)
        return newChar.ID

    def delete(self, charID):
        char = eos.db.getCharacter(charID)
        eos.db.commit()
        eos.db.remove(char)

    def charList(self, charID, userID, apiKey):
        char = eos.db.getCharacter(charID)
        char.apiID = userID
        char.apiKey = apiKey
        try:
            return char.apiCharList()
        except:
            return None

    def apiFetch(self, charID, charName):
        char = eos.db.getCharacter(charID)
        char.apiFetch(charName)
        eos.db.commit()

    def changeLevel(self, charID, skillID, level):
        char = eos.db.getCharacter(charID)
        skill = char.getSkill(skillID)
        if level == "Unlearned":
            skill.learned = False
        else:
            skill.level = level

        eos.db.commit()