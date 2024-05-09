/*
    Copyright (c) 2022 Idiap Research Institute, http://www.idiap.ch/
    Written by Tobias Löw <https://tobiloew.ch>

    This file is part of gafro.

    gafro is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License version 3 as
    published by the Free Software Foundation.

    gafro is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with gafro. If not, see <http://www.gnu.org/licenses/>.
*/

#pragma once

#include <gafro/robot/Manipulator.hpp>
//
#include <gafro_robot_descriptions/serialization/FilePath.hpp>
#include <gafro_robot_descriptions/serialization/SystemSerialization.hpp>
//
#include <filesystem>

namespace gafro
{

    template <class T>
    class FrankaEmikaRobot : public Manipulator<T, 7>
    {
      public:
        FrankaEmikaRobot();

        FrankaEmikaRobot(const std::filesystem::path &assets_folder);

        virtual ~FrankaEmikaRobot();

      protected:
      private:
    };

    template <class T>
    FrankaEmikaRobot<T>::FrankaEmikaRobot()  //
      : Manipulator<T, 7>(std::move(SystemSerialization(FilePath("robots/panda/panda.yaml")).load().cast<T>()), "panda_endeffector_joint")
    {}

    template <class T>
    FrankaEmikaRobot<T>::FrankaEmikaRobot(const std::filesystem::path &assets_folder)
      : Manipulator<T, 7>(std::move(SystemSerialization(FilePath(assets_folder / "robots/panda/panda.yaml")).load().cast<T>()), "panda_endeffector_joint")
    {}

    template <class T>
    FrankaEmikaRobot<T>::~FrankaEmikaRobot()
    {}

}  // namespace gafro