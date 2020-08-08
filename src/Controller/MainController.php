<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\Form\Extension\Core\Type\ColorType;
use Symfony\Component\Form\Extension\Core\Type\IntegerType;
use Symfony\Component\Form\Extension\Core\Type\SubmitType;
use Symfony\Component\Form\Extension\Core\Type\TimeType;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Annotation\Route;

class MainController extends AbstractController
{
    /**
     * @Route("/", name="home_page")
     */
    public function index(Request $request)
    {
        $data = [];

        $fileName = $this->getParameter('kernel.project_dir') . '/py/data.json';

        if (file_exists($fileName)) {

            $json = file_get_contents($fileName);
            $dataArr = json_decode($json, true);
            $r = round($dataArr['rgb1']['r'] * 2.55);
            $g = round($dataArr['rgb1']['g'] * 2.55);
            $b = round($dataArr['rgb1']['b'] * 2.55);

            $rgb = $r * 256 * 256 + $g * 256 + $b;


            $data['color'] = '#' . dechex($rgb);
            $timeOn = new \DateTime($dataArr['timeOn']);
            $data['timeOn'] = $timeOn;
            $timeOff = new \DateTime($dataArr['timeOff']);
            $data['timeOff'] = $timeOff;
            $data['timeOfGradient'] = $dataArr['timeOfGradient'];
        }

        $form = $this->createFormBuilder()
            ->add('color', ColorType::class)
            ->add('timeOn', TimeType::class, ['label' => 'Turn on'])
            ->add('timeOff', TimeType::class, ['label' => 'Turn off'])
            ->add('timeOfGradient', IntegerType::class, ['label' => 'Время плавности (минут)'])
            ->add('submit', SubmitType::class, ['label' => 'Сохранить'])
            ->setData($data)
            ->getForm();

        $form->handleRequest($request);
        if ($form->isSubmitted() && $form->isValid()) {

            $data = $form->getData();

            list($r, $g, $b) = sscanf($data['color'], "#%02x%02x%02x");
            $r = (int)($r / 2.55);
            $g = (int)($g / 2.55);
            $b = (int)($b / 2.55);
            $arr = [
                'rgb1' =>
                    [
                        'r' => $r,
                        'g' => $g,
                        'b' => $b
                    ],
                'timeOn' => $data['timeOn']->format("H:i"),
                'timeOff' => $data['timeOff']->format("H:i"),
                'timeOfGradient' => $data['timeOfGradient'],

            ];
            $json = json_encode($arr);
            $fp = fopen($fileName, "w");
            fwrite($fp, $json);
            fclose($fp);

            return $this->redirectToRoute('home_page');
        }

        return $this->render('main/index.html.twig', [
            'form' => $form->createView(),
        ]);
    }
}
